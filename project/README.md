# AI Agents CrewAI Research Project

This project demonstrates advanced CrewAI patterns for creating AI agent crews that work in both Jupyter notebook environments and standalone Python files. It includes comprehensive examples of decorator usage, configuration management, and troubleshooting approaches.

## 📁 Project Structure

```
project/
├── README.md                           # This file
├── ai-agents-crash-course-part2.ipynb  # Main Jupyter notebook
├── research_crew.py                    # Custom decorators (notebook-compatible)
├── research_crew_with_decorators.py    # Official CrewAI decorators (file-only)
├── config/
│   ├── agents.yaml                     # Agent configurations
│   └── tasks.yaml                      # Task configurations
└── .env                                # Environment variables
```

## 🚨 Why Two Different Research Crew Implementations?

This project includes **two different implementations** of the same research crew functionality to demonstrate the differences between custom and official CrewAI decorators:

### 1. `research_crew.py` - Custom Decorators ✅ Universal Compatibility
- **Uses custom decorators**: `@research_crew_class`, `@research_agent`, `@research_task`, `@research_crew`
- **Works in**: Jupyter notebooks AND standalone Python files
- **Configuration**: Manual YAML loading with error handling
- **Best for**: Development, experimentation, and environments where official decorators fail

### 2. `research_crew_with_decorators.py` - Official CrewAI Decorators ⚠️ File-Only
- **Uses official decorators**: `@CrewBase`, `@agent`, `@task`, `@crew`
- **Works in**: Standalone Python files ONLY
- **Configuration**: Automatic YAML discovery via file path inspection
- **Best for**: Production deployments and traditional Python application structure

## 🎯 Decorator Discussion: Custom vs Official CrewAI Decorators

### The Problem with Official CrewAI Decorators in Jupyter

The official CrewAI decorators (`@CrewBase`, `@agent`, `@task`, `@crew`) have a fundamental limitation when used in **Jupyter notebook environments**:

```python
# This is what happens inside @CrewBase decorator:
import inspect
file_path = inspect.getfile(cls)  # ❌ FAILS in Jupyter notebooks
```

The `@CrewBase` decorator uses Python's `inspect.getfile()` to determine the file path of the class being decorated. This works perfectly in standalone Python files but **fails in Jupyter notebooks** because:

1. **Jupyter cells don't have file paths** - they exist in memory as `<ipython-input-X-hash>`
2. **Dynamic execution context** - code is executed in an interactive namespace
3. **No physical file location** - the decorator can't find YAML config files relative to a non-existent file

### Compatibility Comparison

| Environment | **Official @CrewBase Decorator** | **Custom Decorators** |
|-------------|----------------------------------|----------------------|
| **Standalone .py Files** | ✅ Works | ✅ Works |
| **Jupyter Notebooks** | ❌ Fails | ✅ Works |

### Custom Decorators Design

Our custom decorators work because they:

1. **Don't rely on file path inspection** - they accept config explicitly
2. **Manual configuration loading** - we control when and how YAML files are loaded
3. **Flexible path resolution** - can handle both relative and absolute config paths
4. **Error handling** - graceful fallback when config files aren't found

### Decorator Types for Classes

#### 1. **Official CrewAI Decorator** (File-only)
```python
from crewai import CrewBase, agent, task, crew

@CrewBase
class ResearchCrew:
    """Automatically discovers config/agents.yaml and config/tasks.yaml"""
    
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SerperDevTool()]
        )
```

#### 2. **Custom Functional Decorators** ✅ **Currently implemented**
```python
@research_crew_class
class ResearchCrew:
    """Manual config loading with explicit error handling"""
    
    @research_agent
    def researcher(self) -> Agent:
        return Agent(**self.agents_config['researcher'])
```

#### 3. **Multiple Decorators** (Stacked)
```python
@validation_decorator
@logging_decorator  
@research_crew_class
class ResearchCrew:
    pass
```

#### 4. **Parameterized Decorators**
```python
@research_crew_class(config_path='./config', verbose=True)
class ResearchCrew:
    pass
```

### When to Use Each Approach

#### **Use Official CrewAI Decorators When:**
- Working exclusively with standalone Python files
- Following CrewAI's official patterns and conventions
- Need automatic config discovery and minimal setup
- Deploying to production environments

#### **Use Custom Decorators When:**
- Developing in Jupyter notebooks
- Need explicit control over configuration loading
- Working in mixed environments (notebooks + files)
- Require custom error handling and debugging capabilities
- Prototyping and experimentation

### 🏗️ Current Architecture:

✅ **Class Decorator**: `@research_crew_class` - Enhances the class itself  
✅ **Method Decorators**: `@research_agent`, `@research_task`, `@research_crew` - Mark individual methods  
✅ **Full Compatibility**: Works in notebooks and standalone files  
✅ **Introspection**: Can discover and analyze the class structure automatically  
✅ **No File Dependencies**: Doesn't break in interactive environments

## 🛠️ Setup and Installation

1. **Clone or download** this project
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure environment variables** in `.env`:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   SERPER_DEV_API_KEY=your_serper_api_key_here
   # OR for Ollama
   OLLAMA_API_BASE=http://localhost:11434
   ```

## 🚀 Usage Examples

### In Jupyter Notebooks
```python
# Use the custom decorator version
from research_crew import ResearchCrew

# Initialize and run
crew = ResearchCrew()
result = crew.kickoff({"topic": "AI impact on job markets"})
```

### In Standalone Python Files
```python
# Use either version, but official decorators are recommended
from research_crew_with_decorators import ResearchCrew

# Initialize and run
crew = ResearchCrew()
result = crew.kickoff({"topic": "AI impact on job markets"})
```

## 🔧 Configuration

The project uses YAML configuration files in the `config/` directory:

- **`config/agents.yaml`**: Agent definitions (roles, goals, backstories)
- **`config/tasks.yaml`**: Task definitions (descriptions, expected outputs)

Both implementations support the same configuration structure but load it differently:
- **Custom decorators**: Manual loading with explicit path resolution
- **Official decorators**: Automatic discovery based on file location

## 🐛 Troubleshooting

### Common Issues

1. **ImportError in Jupyter**: Use `research_crew.py` (custom decorators)
2. **Config file not found**: Check file paths and working directory
3. **LiteLLM debug output**: See notebook for debugging and suppression techniques
4. **API key issues**: Verify environment variables are properly set

### Debug Tools

The project includes comprehensive debugging utilities:
- LiteLLM attribute discovery
- Configuration file validation
- Environment variable checking
- Import error diagnosis

## 📚 Learning Resources

This project demonstrates several advanced patterns:
- **Decorator design patterns** for framework integration
- **Multi-environment compatibility** strategies
- **Configuration management** approaches
- **Error handling and debugging** techniques
- **CrewAI best practices** and troubleshooting

## 📄 License

This project is for educational purposes and demonstrates CrewAI usage patterns.

---

**Note**: This project was developed to address real-world challenges when working with CrewAI in different environments, particularly the limitations of official decorators in Jupyter notebook contexts. The dual implementation approach provides maximum flexibility while maintaining compatibility across development scenarios.
