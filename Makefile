# Define the Python interpreter
PYTHON := python3

# Define the tools directory
TOOLS_DIR := Tools

# Define the notebooks directory
NOTEBOOKS_DIR := notebooks

# Define the Python scripts
CREATE_NAVIGATION := $(TOOLS_DIR)/create_navigation.py
GENERATE_CONTENTS := $(TOOLS_DIR)/generate_contents.py
EXECUTE := $(TOOLS_DIR)/execute.py

# Default target
all: create_navigation generate_contents execute

# Target to run create_navigation.py
create_navigation:
	@echo "🚀 Running create_navigation.py"
	@cd $(NOTEBOOKS_DIR) && $(PYTHON) ../$(CREATE_NAVIGATION)
	@echo "✅ Completed create_navigation.py"

# Target to run generate_contents.py
generate_contents:
	@echo "📄 Running generate_contents.py"
	@cd $(NOTEBOOKS_DIR) && $(PYTHON) ../$(GENERATE_CONTENTS)
	@echo "✅ Completed generate_contents.py"

# Target to run execute.py
execute:
	@echo "⚙️ Running execute.py"
	@cd $(NOTEBOOKS_DIR) && $(PYTHON) ../$(EXECUTE)
	@echo "✅ Completed execute.py"

# Clean target (optional)
clean:
	@echo "🧹 Cleaning up..."
	@rm -rf __pycache__
	@echo "✅ Completed cleaning"

.PHONY: all create_navigation generate_contents execute clean