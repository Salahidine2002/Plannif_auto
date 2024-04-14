import json
import pddl_parser.planner as planner
import os
def find_domain_and_problem_files(directory):
    group_files = []

    # Parcourir le répertoire et ses sous-répertoires
    for root, dirs, files in os.walk(directory):
        domain_file = None
        problem_files = []

        # Chercher le fichier de domaine dans le répertoire courant
        for file in files:
            if file.endswith('.pddl') and 'domain' in file:
                domain_file = os.path.join(root, file)
                break

        # Si on a trouvé un fichier de domaine, chercher les fichiers de problèmes dans le même répertoire
        if domain_file:
            for file in files:
                if file.endswith('.pddl') and 'domain' not in file:
                    problem_files.append(os.path.join(root, file))

            # Chercher les fichiers de problèmes dans les sous-répertoires
            for dir in dirs:
                for root_problem, _, files_problem in os.walk(os.path.join(root, dir)):
                    for file in files_problem:
                        if file.endswith('.pddl') and 'domain' not in file:
                            problem_files.append(os.path.join(root_problem, file))

            # Si on a trouvé des fichiers de problèmes, les ajouter à la liste
            if problem_files:
                group_files.append((domain_file, problem_files))
            else:
                print(f"Missing problem files in {root} for domain file {domain_file}")

    return group_files

def execute_pddl_parser(directory, domain_file, problem_files):
    for problem_file in problem_files:
        try:
            # Appeler la fonction main du planner directement
            print(f'le planner va être exécuté pour le fichier de domaine {domain_file} et le fichier de problème {problem_file}')
            results = planner.main(domain_file, problem_file)
            # Écrire les résultats dans un fichier JSON
            group_folder = 'problem_results'
            os.makedirs(group_folder, exist_ok=True)

            # Enregistrez le résultat dans un fichier JSON dans le sous-dossier du groupe
            base_name = os.path.splitext(os.path.basename(problem_file))[0]
            with open(os.path.join(group_folder, base_name + '.json'), 'w') as f:
                json.dump(results, f)
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'exécution du planner pour le fichier de domaine {domain_file} et le fichier de problème {problem_file}. L'erreur est : {e}")

directory = "./"
group_files = find_domain_and_problem_files(directory)

for domain_file, problem_files in group_files:
    #print(f"domain_file = {domain_file}, problem_files = {problem_files}")
    execute_pddl_parser(directory, domain_file, problem_files) #