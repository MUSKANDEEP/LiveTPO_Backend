from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'username', 'email', 'contact', 'phone', 'course', 'cgpa',
            'is_verified', 'verification_token', 'tenth_board', 'tenth_percentage', 
            'twelfth_board', 'twelfth_percentage', 'year_of_graduation', 'university',
            'skills', 'resume_link', 'github_link', 'linkedin_link', 'portfolio_link', 
            'certifications', 'projects', 'achievements', 'languages_known',
            'preferred_job_location', 'relocation_ready', 'preferred_company_type',
            'applied_companies', 'availability_date', 'created_at', 'updated_at',
            'image_url', 'placement_status', 'offers', 'placement_history'  # Added new fields
        ]
        read_only_fields = ('password',)  # Ensure password is not included in the response

    def get_image_url(self, obj):
        # Check if the student has an image and return its URL, else return None
        if obj.image:
            return obj.image.url
        return None

    # Optional: You can add custom validation for the placement status if needed.
    def validate_placement_status(self, value):
        if value not in ['Pending', 'Placed']:
            raise serializers.ValidationError("Placement status must be 'Pending' or 'Placed'.")
        return value

    # Optional: Custom validation for offers or placement history (if it's needed)
    def validate_offers(self, value):
        # Example: Ensure offers is a list of dictionaries with the correct keys.
        for offer in value:
            if 'company_name' not in offer or 'job_role' not in offer or 'ctc' not in offer:
                raise serializers.ValidationError("Each offer must contain 'company_name', 'job_role', and 'ctc'.")
        return value

    def validate_placement_history(self, value):
        # Example: Ensure placement history contains valid data
        for history in value:
            if 'company_name' not in history or 'status' not in history or 'year' not in history:
                raise serializers.ValidationError("Each placement history entry must contain 'company_name', 'status', and 'year'.")
        return value
