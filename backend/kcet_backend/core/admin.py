from  django.contrib import admin
from core.utils.excel_export import export_to_excel
from core.infrastructure.django_models.communication import Subscriber, ApprovedGmail
from core.infrastructure.django_models.colleges import College
from core.infrastructure.django_models.Branch import Branch
from core.infrastructure.django_models.Branch_college import CollegeBranch
from core.infrastructure.django_models.category import Category
from core.infrastructure.django_models.Round import Round
from core.infrastructure.django_models.Year import Year
from core.infrastructure.django_models.Cutoff import Cutoff
from core.infrastructure.django_models.seat_matrix import SeatMatrix
from core.services.ingestors.branch_ingestor import BranchIngestor
from core.services.ingestors.cutoff_ingestor import CutoffIngestor 
from core.services.preprocessing.cutoff_preprocessor import  CutoffDataPreprocessor
from core.services.ingestors.college_branch_ingestor import CollegeBranchIngestor
from core.services.ingestors.seatmatrix_ingestor import SeatMatrixIngestor
from django.contrib import admin, messages
admin.site.register([ Category, Round, Year])
from django.shortcuts import render, redirect
from django.contrib import admin
from django.utils.timezone import now
from django.conf import settings
from django.core.mail import send_mail
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
from core.infrastructure.django_models.roles import User

from core.models import Subscriber, ApprovedGmail


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "is_approved", "created_at", "approved_at")
    list_filter = ("is_approved",)
    search_fields = ("email",)
    actions = ["approve_subscribers"]

    @admin.action(description="Approve selected subscribers and send email")
    def approve_subscribers(self, request, queryset):
        for subscriber in queryset.filter(is_approved=False):
            subscriber.is_approved = True
            subscriber.approved_at = now()
            subscriber.save(update_fields=["is_approved", "approved_at"])

            send_mail(
                subject="KCET Companion – Subscription Approved ✅",
                message=(
                    "Hello,\n\n"
                    "Your KCET Companion subscription has been approved!\n\n"
                    "You will now start receiving important updates, alerts, "
                    "and study resources.\n\n"
                    "Best regards,\n"
                    "KCET Companion Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber.email],
                fail_silently=False,
            )


@admin.register(ApprovedGmail)
class ApprovedGmailAdmin(admin.ModelAdmin):
    list_display = ("email", "approved")
    list_filter = ("approved",)
    search_fields = ("email",)
    actions = ["mark_as_approved"]

    @admin.action(description="Mark selected emails as approved")
    def mark_as_approved(self, request, queryset):
        queryset.update(approved=True)

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    change_list_template = "admin/branch_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("ingest/", self.admin_site.admin_view(self.ingest_view), name="branch_ingest"),
        ]
        return custom_urls + urls

    def ingest_view(self, request):
        if request.method == "POST":
            try:
                BranchIngestor().run()
                self.message_user(request, "Branch ingestion completed successfully", messages.SUCCESS)
                return redirect("..")
            except Exception as e:
                self.message_user(request, str(e), messages.ERROR)

        return render(request, "admin/branch_ingest_form.html")
    
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages

from core.services.ingestors.college_ingestor import CollegePreprocessor, CollegeIngestor
from core.models import College


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = (
        "college_code",
        "College_name",
        "location",
        "naaccrating",
        "Rating",
    )

    change_list_template = "admin/college_changelist.html"

    actions = ["download_excel"]

    # ------------------------
    # Custom Admin URLs
    # ------------------------
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("ingest/", self.admin_site.admin_view(self.ingest_colleges)),
        ]
        return custom_urls + urls

    # ------------------------
    # Ingest Colleges
    # ------------------------
    def ingest_colleges(self, request):
        try:
            processor = CollegePreprocessor(
                scrape_url="https://collegedunia.com/btech/karnataka-colleges?exam_id=61",
                official_excel=r"C:\Users\mahes\OneDrive\Desktop\kcet_companion\backend\kcet_backend\core\data\collegedunia_college_names.xlsx",
                sheet_index=3,
            )

            df = processor.run()
            ingestor = CollegeIngestor(df)
            report = ingestor.ingest()

            messages.success(
                request,
                f"Ingestion complete — "
                f"Created: {report['created']} | "
                f"Updated: {report['updated']} | "
                f"Skipped: {report['skipped']}"
            )

        except Exception as e:
            messages.error(request, f"Ingestion failed: {e}")

        return redirect("..")

    # ------------------------
    # Download Selected as Excel
    # ------------------------
    @admin.action(description="Download selected colleges as Excel")
    def download_excel(self, request, queryset):
        fields = [
            "college_code",
            "College_name",
            "location",
            "naaccrating",
            "Rating",
        ]
        return export_to_excel(queryset, fields, "college_data")



@admin.register(CollegeBranch)
class CollegeBranchAdmin(admin.ModelAdmin):

    change_list_template = "admin/collegebranch_changelist.html"
    list_display = ("code_branch", "college", "branch")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("ingest/", self.admin_site.admin_view(self.ingest_view), name="collegebranch_ingest"),
        ]
        return custom_urls + urls

    def ingest_view(self, request):
        if request.method == "POST":
            try:
                count = CollegeBranchIngestor().run()
                self.message_user(request, f"✅ {count} College-Branch records created", messages.SUCCESS)
                return redirect("..")
            except Exception as e:
                self.message_user(request, str(e), messages.ERROR)

        return render(request, "admin/collegebranch_ingest_form.html")
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from core.services.ingestors.cutoff_ingestor import CutoffIngestor
from core.models import Cutoff


@admin.register(Cutoff)
class CutoffAdmin(admin.ModelAdmin):
    list_display=[
        "college_branch",
        "category",
        "round",
        "year",
        "rank"
    ]
    list_filter=[
        "category",
        "round",
        "year",
    ]
    change_list_template = "admin/cutoff_changelist.html"
    actions = ["download_excel"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("ingest/", self.admin_site.admin_view(self.ingest_view), name="cutoff_ingest"),
        ]
        return custom_urls + urls

    def ingest_view(self, request):
        if request.method == "POST":
            try:
                file_path = request.POST["file_path"]
                round_type = request.POST["round_type"]
                year = int(request.POST["year"])

                from core.services.ingestors.cutoff_ingestor import CutoffIngestor
                CutoffIngestor(file_path, round_type, year).run()

                self.message_user(request, "✅ Cutoff data ingested successfully", messages.SUCCESS)
                return redirect("..")

            except Exception as e:
                self.message_user(request, f"❌ Ingestion failed: {e}", messages.ERROR)

        return render(request, "admin/cutoff_ingest_form.html")
    def download_excel(self, request, queryset):
        fields = [ 
        "college_branch",
        "category",
        "round",
        "year",
        "rank"
        ]
        return export_to_excel(queryset, fields, "cutoff_data")


from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
from core.models import SeatMatrix

from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
import tempfile, os

from core.models import SeatMatrix
from core.services.ingestors.seatmatrix_ingestor import SeatMatrixIngestor
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path
import tempfile, os

from core.models import SeatMatrix
from core.services.ingestors.seatmatrix_ingestor import SeatMatrixIngestor


@admin.register(SeatMatrix)
class SeatMatrixAdmin(admin.ModelAdmin):

    list_display = (
        "college_branch",
        "year",
        "category",
        "round",
        "total_seats",
        "filled_seats",
        "available_seats",
        "last_updated",
    )
    list_filter = (
        "year",
        "round",
        "category",
        "college_branch__college",
        "college_branch__branch",
    )
    ordering = ("-year", "college_branch__college__College_name")

    change_list_template = "admin/seatmatrix_changelist.html"

    actions = ["download_excel"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("ingest/", self.admin_site.admin_view(self.ingest_view), name="seatmatrix_ingest"),
        ]
        return custom_urls + urls

    def ingest_view(self, request):
        if request.method == "POST":
            try:
                upload = request.FILES["file"]
                year = request.POST["year"]
                round_code = request.POST["round"]

                with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                    for chunk in upload.chunks():
                        tmp.write(chunk)
                    temp_path = tmp.name

                SeatMatrixIngestor(temp_path, round_code, year).run()

                os.remove(temp_path)

                self.message_user(request, "✅ Seat Matrix ingested successfully", messages.SUCCESS)
                return redirect("..")

            except Exception as e:
                self.message_user(request, f"❌ Ingestion failed: {e}", messages.ERROR)

        return render(request, "admin/seatmatrix_ingest_form.html")
    def download_excel(self, request, queryset):
        fields = [ "college_branch",
        "year",
        "category",
        "round",
        "total_seats",
        "filled_seats",
        "available_seats",
        ]
        return export_to_excel(queryset, fields, "seat_matrix_data")

    download_excel.short_description = "⬇️ Download Selected as Excel"

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    # 🔹 Columns shown in admin list
    list_display = (
        "email",
        "role",
        "is_approved",
        "is_active",
        "is_staff",
    )

    # 🔹 Filters on right side
    list_filter = (
        "role",
        "is_approved",
        "is_active",
        "is_staff",
    )

    # 🔹 Search box
    search_fields = ("email",)

    # 🔹 Default ordering
    ordering = ("email",)

    # 🔹 Fields when editing a user
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Role & Approval", {"fields": ("role", "is_approved")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("OTP / Session", {"fields": ("otp", "otp_expires_at", "current_session_id")}),
    )

    # 🔹 Fields when creating a new user
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "role",
                "is_approved",
                "is_active",
                "is_staff",
            ),
        }),
    )

    USERNAME_FIELD = "email"
