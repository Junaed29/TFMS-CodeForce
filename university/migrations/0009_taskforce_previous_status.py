from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0008_taskforce_psm_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskforce',
            name='previous_status',
            field=models.CharField(blank=True, choices=[('ACTIVE', 'Active'), ('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted for Approval'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('INACTIVE', 'Inactive')], max_length=20, null=True),
        ),
    ]
