from django.db import migrations, models


def split_hod_justification(apps, schema_editor):
    TaskForce = apps.get_model('university', 'TaskForce')
    marker = '[Justification]:'
    for tf in TaskForce.objects.filter(description__contains=marker):
        description = tf.description or ''
        before, after = description.split(marker, 1)
        cleaned_desc = before.rstrip()
        justification = after.strip()
        updates = {}
        if justification and not tf.hod_justification:
            updates['hod_justification'] = justification
        updates['description'] = cleaned_desc or None
        if updates:
            for field, value in updates.items():
                setattr(tf, field, value)
            tf.save(update_fields=list(updates.keys()))


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0009_taskforce_previous_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskforce',
            name='hod_justification',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RunPython(split_hod_justification, migrations.RunPython.noop),
    ]
