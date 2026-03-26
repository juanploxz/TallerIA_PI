from django.db import migrations, models
import movie.models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_alter_movie_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='emb',
            field=models.BinaryField(default=movie.models.get_default_embedding_bytes),
        ),
        migrations.AlterField(
            model_name='movie',
            name='description',
            field=models.CharField(blank=True, max_length=1500),
        ),
        migrations.AlterField(
            model_name='movie',
            name='image',
            field=models.ImageField(default='movie/images/default.JPG', upload_to='movie/images/'),
        ),
    ]
