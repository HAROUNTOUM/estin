from .models import Module

def run():
    # Example data structure
    data = {
        ('1CP', 'S1'): ['Maths 1', 'Physique 1', 'Informatique 1'],
        ('1CP', 'S2'): ['Maths 2', 'Physique 2', 'Bureautique'],
        ('2CP', 'S1'): ['Algebre', 'Analyse', 'Electronique'],
    }

    for (lvl, sem), names in data.items():
        for name in names:
            Module.objects.get_or_create(name=name, level=lvl, semester=sem)
    print("Modules populated successfully!")
