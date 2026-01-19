from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Reservation
from .serializers import ReservationSerializer
from courses.models import Cours
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from users.models import Utilisateurs  # For coach notifications


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling reservations.
    - Users can view their own reservations
    - Admins can view all reservations
    - Users can create reservations (with validation)
    """
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return reservations based on user role:
        - Admin: all reservations
        - Other users: only their own reservations
        """
        if self.request.user.role == 'administrateur':
            return Reservation.objects.all().select_related('id_Utilisateur', 'id_Cour')
        return Reservation.objects.filter(id_Utilisateur=self.request.user).select_related('id_Utilisateur', 'id_Cour')

    def create(self, request):
        """
        Create a new reservation with validation:
        1. Check if course exists
        2. Check if user already reserved this course
        3. Check if course has available capacity
        4. Create reservation
        5. Update course capacity
        6. Send notification to coach (if any)
        """
        try:
            # 1. Validate Course
            try:
                course_id = request.data.get('id_Cour')
                if not course_id:
                    return Response({"error": "Le champ 'id_Cour' est requis"}, status=status.HTTP_400_BAD_REQUEST)

                cours = Cours.objects.get(id=course_id)
            except Cours.DoesNotExist:
                return Response({"error": "Cours introuvable"}, status=status.HTTP_404_NOT_FOUND)

            # 2. Check if user already reserved this course
            existing_reservation = Reservation.objects.filter(
                id_Utilisateur=request.user,
                id_Cour=cours
            ).first()

            if existing_reservation:
                return Response({
                    "error": "Vous avez déjà réservé ce cours",
                    "reservation_id": existing_reservation.id,
                    "statut": existing_reservation.statut
                }, status=status.HTTP_400_BAD_REQUEST)

            # 3. Check Capacity
            if cours.est_complet():
                return Response({
                    "error": "Cours complet",
                    "places_disponibles": cours.places_disponibles(),
                    "capacite_max": cours.capacite_max
                }, status=status.HTTP_400_BAD_REQUEST)

            # 4. Create Reservation
            reservation = Reservation.objects.create(
                id_Utilisateur=request.user,
                id_Cour=cours,
                statut='confirmée'
            )

            # 5. Update Course Capacity
            cours.placesoccupees = Cours.objects.filter(id=cours.id).values_list('placesoccupees',
                                                                                 flat=True).first() or 0
            cours.placesoccupees += 1
            cours.save(update_fields=['placesoccupees'])

            # 6. Send Real-time Notification to the Coach (if course has a coach)
            try:
                if cours.id_Utilisateur:
                    channel_layer = get_channel_layer()
                    coach = cours.id_Utilisateur
                    message_content = f"Nouvelle réservation pour le cours '{cours.nom}' par {request.user.username}"

                    async_to_sync(channel_layer.group_send)(
                        f"notifications_{coach.id}",  # Match the NotificationConsumer group name
                        {
                            "type": "send_notification",
                            "message": message_content
                        }
                    )

                    # Also create a Notification record in database
                    from notifications.models import Notifications
                    Notifications.objects.create(
                        titre="Nouvelle réservation",
                        message=message_content
                        # Note: If you add user field to Notifications model, add: user=coach
                    )
            except Exception as e:
                # Don't fail the reservation if notification fails
                print(f"Notification error (non-critical): {e}")

            return Response(
                ReservationSerializer(reservation).data,
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            # Log the full error for debugging
            import traceback
            print(f"Reservation error: {e}")
            print(traceback.format_exc())

            return Response(
                {"error": "Une erreur interne est survenue", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        """
        Cancel a reservation.
        Only the reservation owner or admin can cancel.
        """
        try:
            reservation = self.get_object()

            # Check permissions
            if request.user != reservation.id_Utilisateur and request.user.role != 'administrateur':
                return Response(
                    {"error": "Vous n'êtes pas autorisé à annuler cette réservation"},
                    status=status.HTTP_403_FORBIDDEN
                )

            # Check if reservation can be cancelled
            if reservation.statut == 'annulée':
                return Response(
                    {"error": "Cette réservation est déjà annulée"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update reservation status
            reservation.statut = 'annulée'
            reservation.save(update_fields=['statut'])

            # Free up the spot in the course
            cours = reservation.id_Cour
            if cours.placesoccupees > 0:
                cours.placesoccupees -= 1
                cours.save(update_fields=['placesoccupees'])

            return Response(
                {"message": "Réservation annulée avec succès", "reservation": ReservationSerializer(reservation).data},
                status=status.HTTP_200_OK
            )

        except Reservation.DoesNotExist:
            return Response(
                {"error": "Réservation introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def mark_present(self, request, pk=None):
        """
        Mark a member as present for the course (admin/coach only).
        """
        try:
            reservation = self.get_object()
            reservation.present = True
            reservation.save(update_fields=['present'])

            return Response(
                {"message": f"{reservation.id_Utilisateur.username} marqué comme présent",
                 "reservation": ReservationSerializer(reservation).data},
                status=status.HTTP_200_OK
            )

        except Reservation.DoesNotExist:
            return Response(
                {"error": "Réservation introuvable"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )