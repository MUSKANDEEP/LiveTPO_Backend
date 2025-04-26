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
            'applied_companies', 'availability_date', 'created_at', 'updated_at', 'image_url'
        ]
        read_only_fields = ('password',)  # Ensure password is not included in the response

    def get_image_url(self, obj):
        # Check if the student has an image and return its URL, else return None
        if obj.image:
            return obj.image.url
        return None
