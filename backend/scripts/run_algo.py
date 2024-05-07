import argparse
from datetime import date

from app import crud
from app.algo.default import algorithms
from app.dependencies import ContextManager




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("algo_type", help="Algorithm to use",
                        type=str, choices=algorithms.keys())
    parser.add_argument("-d", "--date", 
                        help="Date to assign in YYYY-MM-DD. Defaults to today.", 
                        default=date.today(),
                        type=date.fromisoformat)
    args = parser.parse_args()
    
    with ContextManager() as db:
        algorithm = algorithms[args.algo_type]
        crud.update_bookings_on_date(db, args.date, algorithm)
        print(f"Algorithm {args.algo_type} ran for bookings on {args.date}")