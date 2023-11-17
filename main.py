import src.obtain
import src.scrub
import src.make_dataset
import src.model
import src.interpret

# python main.py
if __name__ == "__main__":
    src.obtain.run()
    src.scrub.run()
    src.make_dataset.run()
    src.model.run()
    src.interpret.run()