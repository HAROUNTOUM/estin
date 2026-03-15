from django.db import migrations


def populate_modules(apps, schema_editor):
    Module = apps.get_model('froms', 'Module')

    data = {
        ('1CP', 'S2'): [
            'Analyse mathématique 2',
            'Mécanique du point',
            'Algebre 2',
            'Algorithmique et structures de données dynamiques',
            'English 2',
            'Electronique fondamentale 1',
            'Introduction au Système d_exploitation 2',
        ],
        ('1CS', 'S1'): [
            'RX1',
            'BDD',
            'RO1',
            'SE',
            'PAFA',
            'ANG',
            'ThL',
            'GL',
        ],
        ('1CS', 'S2'): [
            'MF',
            'ANUM',
            'Entreprenariat',
            'SEC',
            'RX2',
            'IA',
            'ADCI',
            'RO2',
        ],
        ('2CP', 'S1'): [
            'économie',
            'Structure Fichiers et Structure de Données',
            'Algebra 3',
            'Analyse Mathématique 3',
            'Probabilités et Statistiques 1',
            'Electronique Fondamentale 2',
            'Architecture des Ordinateurs 2',
        ],
        ('2CP', 'S2'): [
            'Projet Pluridisciplinaire',
            'Probabilités et Statistiques 2',
            'Logique Mathématique',
            'Programmation Orientée Objet (POO,OOP)',
            'Introduction aux systèmes d_information',
            'Analyse Mathématique 4',
            'Optique et Ondes électromagnétiques',
        ],
        ('2CS', 'S1'): [
            'EN',
            'ANAD',
            'DS',
            'Complexité',
            'Cloud',
            'GL',
            'Projet',
            'BDDA',
        ],
        ('2CS', 'S2'): [
            'S2(CS)',
            'S2(IA)',
        ],
        ('3CS', 'S1'): [
            'S1(CS)',
            'S1(IA)',
        ],
    }

    for (level, semester), names in data.items():
        for name in names:
            Module.objects.get_or_create(
                name=name,
                level=level,
                semester=semester,
            )


def remove_modules(apps, schema_editor):
    Module = apps.get_model('froms', 'Module')
    Module.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('froms', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_modules, reverse_code=remove_modules),
    ]
