# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-29 15:16
from __future__ import unicode_literals

import cms.models.streamfield
from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0023_alter_page_revision_on_delete_behaviour'),
        ('wagtailimages', '0010_change_on_delete_behaviour'),
        ('wagtaildocs', '0004_capitalizeverbose'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('body', wagtail.core.fields.StreamField([(b'h2', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h3', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'h4', wagtail.core.blocks.CharBlock(classname='title', icon='title')), (b'intro', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'paragraph', wagtail.core.blocks.RichTextBlock(icon='pilcrow')), (b'aligned_image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.RichTextBlock()), (b'alignment', cms.models.streamfield.ImageFormatChoiceBlock())], icon='image', label='Aligned image')), (b'pullquote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.TextBlock('quote title')), (b'attribution', wagtail.core.blocks.CharBlock())])), (b'document', wagtail.documents.blocks.DocumentChooserBlock(icon='doc-full-inverse')), (b'aligned_html', wagtail.core.blocks.StructBlock([(b'html', wagtail.core.blocks.RawHTMLBlock()), (b'alignment', cms.models.streamfield.HTMLAlignmentChoiceBlock())], icon='code', label='Raw HTML'))])),
            ],
            options={
                'verbose_name': 'Homepage',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePageCarouselItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, null=True, verbose_name='External link')),
                ('embed_url', models.URLField(blank=True, verbose_name='Embed URL')),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
                ('link_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtaildocs.Document')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='carousel_items', to='cms.HomePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HomePageRelatedLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('link_external', models.URLField(blank=True, null=True, verbose_name='External link')),
                ('title', models.CharField(help_text='Link title', max_length=256)),
                ('link_document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtaildocs.Document')),
                ('link_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailcore.Page')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_links', to='cms.HomePage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
