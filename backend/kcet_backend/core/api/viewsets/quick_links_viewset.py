from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

class QuickLinksViewSet(ViewSet):
    def list(self, request):
        links = [
            {
                "title": "Apply for KCET 2026",
                "url": "https://cetonline.karnataka.gov.in/",
                "icon": "fa-pen",
                "highlight": True
            },
            {
                "title": "KCET Counselling Portal",
                "url": "https://cetonline.karnataka.gov.in/",
                "icon": "fa-users",
                "highlight": False
            },
            {
                "title": "KCET Official Website",
                "url": "https://kea.kar.nic.in/",
                "icon": "fa-globe",
                "highlight": False
            }
        ]

        return Response({
            "quick_links": links   # 👈 only once
        })
