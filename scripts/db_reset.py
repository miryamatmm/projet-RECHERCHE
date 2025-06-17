from common import *
backend_path = os.path.abspath(os.path.join(os.path.join(os.path.dirname(__file__), ".."), "backend"))
sys.path.insert(0, backend_path)

from env import *
from database import *

def main():
    run_admin_command("docker pull postgres")

    if is_service_running("postgres"):
        stop = input(f"The service postgres is running. Do you want to stop it? (yes/no): ")
        if stop.lower() == "yes":
            run_admin_command("docker compose down postgres")
            logger.info("Service stopped.")
        else:
            exit()
    logger.info("Removing folders...")
    remove_folder('data')
    remove_folder('uploads')
    create_folder('uploads')
    run_admin_command("docker compose up -d postgres")
    time.sleep(DB_STARTUP_TIME)
    init_db()

def init_db():
    init_db_tables()
    init_db_data()


def init_db_tables():
    "Create db tables using the ORM"
    engine = get_db_engine();
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    logger.info(f"Tables in the database: {tables}")

def init_db_data():
    "Insert static data in the database"
    db = next(get_db())     
    # Check if there are universities already in the database
    if db.query(University).count() or db.query(Discipline).count():
            logger.error("Trying to init db data but some static data are already exist in the database. Skipping initialization.")
            return

    logger.info("Inserting disciplines...")
    from default_knowledge_tree import __common, biology #, computer_science, mathematics, physics
    trees = [biology.tree] #, computer_science.tree, mathematics.tree, physics.tree]
    for tree in trees:
        __common.insert_tree(db, Discipline, tree)
    logger.info("Disciplines inserted successfully.")
    
    
    logger.info("Inserting universities...")
    ucbl = University(name="Université Claude Bernard Lyon 1", country="France", website="https://www.univ-lyon1.fr/")
    universities = [
        ucbl,
        University(name="University of Granada", country="Spain", website="https://www.ugr.es/"),
        University(name="University of Graz", country="Austria", website="https://www.uni-graz.at/en/"),
        University(name="Leipzig University", country="Germany", website="https://www.uni-leipzig.de/en/"),
        University(name="Maynooth University", country="Ireland", website="https://www.maynoothuniversity.ie/"),
        University(name="University of Minho", country="Portugal", website="https://www.uminho.pt/EN"),
        University(name="University of Padua", country="Italy", website="https://www.unipd.it/en/"),
        University(name="Vilnius University", country="Lithuania", website="https://www.vu.lt/en/"),
        University(name="University of Wrocław", country="Poland", website="https://www.uni.wroc.pl/en/"),
    ]
    db.add_all(universities)
    db.commit()
    logger.info("Universities added successfully.")
    supervisors = [
        InternshipSupervisor(firstname="Alice", 
                             lastname="Smith", 
                             role=SupervisorRoleEnum.masters_director, 
                             email="alice.smith@test.edu", 
                             university_id=ucbl.id),
        InternshipSupervisor(firstname="Bob", 
                             lastname="Johnson", 
                             role=SupervisorRoleEnum.internship_manager, 
                             email="bob.johnson@test.edu", 
                             university_id=ucbl.id),
        InternshipSupervisor(firstname="Charlie", 
                             lastname="Davis", 
                             role=SupervisorRoleEnum.researcher,
                             email="charlie.davis@test.edu",
                             university_id=ucbl.id),
        InternshipSupervisor(firstname="David",
                             lastname="Martinez",
                             role=SupervisorRoleEnum.masters_director,
                             email="david.martinez@test.edu",
                             university_id=ucbl.id),
    ]
    db.add_all(supervisors)
    db.commit()
    db.close()
    print("Inserted 5 test InternshipSupervisors successfully.")
    
    db.commit()

if __name__ == "__main__":
    main()