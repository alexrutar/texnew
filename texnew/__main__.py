from .parse import parse
import sys
            
def main():
    """Script entry point"""
    l = Launcher()

    if len(sys.argv) == 2:
        l.override_args()
    else:
        l.check()
        l.initialize_args()
        l.launch()

if __name__ == "__main__":
    parse()
