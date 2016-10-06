from __future__ import unicode_literals
from django.db import migrations, models

import acra.django


def migrate_emails(apps, schema_editor):
    if not schema_editor.connection.alias == 'default':
        return
    member_app = apps.get_app_config('members')
    CorporateMember = member_app.get_model('CorporateMember')
    for column_name in ['contact_email', 'billing_email']:
        schema_editor.execute(
            'alter table "{table}" '
            'alter column "{column}" '
            'type bytea using convert_to("{column}", \'utf-8\');'.format(
                table=CorporateMember._meta.db_table, column=column_name))

    DeveloperMember = member_app.get_model('DeveloperMember')
    schema_editor.execute(
        'alter table "{table}" '
        'alter column "{column}" '
        'type bytea using convert_to("{column}", \'utf-8\');'.format(
        table=DeveloperMember._meta.db_table, column='email'))


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_corporatemember_django_usage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corporatemember',
            name='django_usage',
            field=models.TextField(blank=True, help_text='Not displayed publicly.'),
        ),
        # drop unique index
        migrations.AlterField(
            model_name='developermember',
            name='email',
            field=models.EmailField(max_length=254),
        ),
        migrations.RunPython(migrate_emails),
    ]
