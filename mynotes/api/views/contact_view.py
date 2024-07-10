from rest_framework.response import Response
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from api.serializers.group_serializer import *
from api.models import Contact
from api.serializers.contact_serializer import ContactSerializer

class ContactListPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 50

    def get_paginated_response(self, data):
        return Response({
            'page_info': {
                'links': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link()
                },
                'count': self.page.paginator.count,
                'current_page_number': self.page.number,
                'last_page_number': self.page.paginator.num_pages
            },
            'data': data
        })
    
class ContactListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ContactListPagination
    serializer_class = ContactSerializer

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(user_from=user).union(Contact.objects.filter(user_to=user))
    
    
class ContactDetailsView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContactSerializer
    lookup_field = 'id'

    def get_object(self):
        return generics.get_object_or_404(Contact, id=self.kwargs['id'])
