from rest_framework.response import Response
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from api.serializers.group_serializer import *
from api.permissions import IsMember, IsOwner

class GroupListPagination(PageNumberPagination):
    page_size = 10
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

class GroupListView(generics.ListCreateAPIView):
    """
    Creating new Group
    """
    permission_classes = [IsAuthenticated]
    search_fields = ['name']
    pagination_class = GroupListPagination
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(members=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            user = self.request.user
            group = serializer.save()
            group.members.add(user)
            group.owners.add(user)
        else:
            print('serializer error')


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GroupCreateUpdateSerializer
        return GroupDetailsSerializer
    
class GroupDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """
    Managing Group, Owners only
    """
    lookup_field = 'id'
    serializer_class = GroupDetailsSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GroupDetailsSerializer
        return GroupCreateUpdateSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsMember()]
        return [IsOwner()]
    
    def get_object(self):
        obj = generics.get_object_or_404(Group, id=self.kwargs['id'])
        self.check_object_permissions(self.request, obj)
        return obj