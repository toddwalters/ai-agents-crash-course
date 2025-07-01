from crewai import Agent, Crew, Task, Process
from crewai_tools import SerperDevTool
import yaml


# Custom decorators that work in all environments
def research_crew_class(cls):
    """Decorator to mark and enhance a research crew class.

    Args:
        cls: The class to be decorated

    Returns:
        The enhanced class with additional metadata and methods
    """
    cls._is_research_crew = True  # pylint: disable=protected-access
    cls._crew_type = "research"  # pylint: disable=protected-access

    # Add metadata
    cls._created_at = "2025"  # pylint: disable=protected-access
    cls._version = "1.0"  # pylint: disable=protected-access

    # Add class methods for introspection
    def get_crew_info(cls):
        """Get information about this crew class.

        Returns:
            dict: Dictionary containing crew metadata including name, type, version, 
                  creation date, and counts of agents and tasks
        """
        return {
            "name": cls.__name__,
            "type": getattr(cls, '_crew_type', 'unknown'),
            "version": getattr(cls, '_version', '0.0'),
            "created": getattr(cls, '_created_at', 'unknown'),
            "agents": len(cls.get_agent_methods()),
            "tasks": len(cls.get_task_methods())
        }

    def get_agent_methods(cls):
        """Get all agent methods in the class.

        Returns:
            list: List of method names that are decorated as agents
        """
        return [name for name in dir(cls)
                if hasattr(getattr(cls, name), '_is_agent')]

    def get_task_methods(cls):
        """Get all task methods in the class.

        Returns:
            list: List of method names that are decorated as tasks
        """
        return [name for name in dir(cls)
                if hasattr(getattr(cls, name), '_is_task')]

    # Bind methods to class
    cls.get_crew_info = classmethod(get_crew_info)
    cls.get_agent_methods = classmethod(get_agent_methods)
    cls.get_task_methods = classmethod(get_task_methods)

    return cls


def research_agent(func):
    """Decorator to mark a method as an agent.

    Args:
        func: The method to be decorated

    Returns:
        The decorated method with _is_agent attribute set to True
    """
    func._is_agent = True  # pylint: disable=protected-access
    return func


def research_task(func):
    """Decorator to mark a method as a task.

    Args:
        func: The method to be decorated

    Returns:
        The decorated method with _is_task attribute set to True
    """
    func._is_task = True  # pylint: disable=protected-access
    return func


def research_crew(func):
    """Decorator to mark a method as the crew builder.

    Args:
        func: The method to be decorated

    Returns:
        The decorated method with _is_crew attribute set to True
    """
    func._is_crew = True  # pylint: disable=protected-access
    return func


@research_crew_class
class ResearchCrew:
    """A crew for conducting research, summarizing findings, and fact-checking.

    This class provides a complete research workflow with three specialized agents:
    - Research Agent: Conducts web-based research using SerperDevTool
    - Summarization Agent: Condenses research findings into clear summaries
    - Fact Checker Agent: Validates information accuracy using additional searches

    Attributes:
        search_tool (SerperDevTool): Tool for web-based research and fact-checking
        agents_config (dict): Configuration loaded from config/agents.yaml
        tasks_config (dict): Configuration loaded from config/tasks.yaml
    """

    def __init__(self):
        """Initialize the ResearchCrew with search tools and configuration."""
        self.search_tool = SerperDevTool()

        # Load configuration files manually
        with open('config/agents.yaml', 'r', encoding='utf-8') as f:
            self.agents_config = yaml.safe_load(f)

        with open('config/tasks.yaml', 'r', encoding='utf-8') as f:
            self.tasks_config = yaml.safe_load(f)

    @research_agent
    def research_agent_method(self) -> Agent:
        """Create and return the research agent.

        Returns:
            Agent: Configured research agent with web search capabilities
        """
        config = self.agents_config['research_agent']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            tools=[self.search_tool],
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False)
        )

    @research_agent
    def summarization_agent_method(self) -> Agent:
        """Create and return the summarization agent.

        Returns:
            Agent: Configured summarization agent for condensing research findings
        """
        config = self.agents_config['summarization_agent']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False)
        )

    @research_agent
    def fact_checker_agent_method(self) -> Agent:
        """Create and return the fact-checking agent.

        Returns:
            Agent: Configured fact-checking agent with web search capabilities
        """
        config = self.agents_config['fact_checker_agent']
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            tools=[self.search_tool],
            verbose=config.get('verbose', True),
            allow_delegation=config.get('allow_delegation', False)
        )

    @research_task
    def research_task_method(self) -> Task:
        """Create and return the research task.

        Returns:
            Task: Configured task for conducting web-based research
        """
        config = self.tasks_config['research_task']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            tools=[self.search_tool],
            agent=self.research_agent_method()
        )

    @research_task
    def summarization_task_method(self) -> Task:
        """Create and return the summarization task.

        Returns:
            Task: Configured task for summarizing research findings
        """
        config = self.tasks_config['summarization_task']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            agent=self.summarization_agent_method()
        )

    @research_task
    def fact_checking_task_method(self) -> Task:
        """Create and return the fact-checking task.

        Returns:
            Task: Configured task for validating information accuracy
        """
        config = self.tasks_config['fact_checking_task']
        return Task(
            description=config['description'],
            expected_output=config['expected_output'],
            tools=[self.search_tool],
            agent=self.fact_checker_agent_method()
        )

    @research_crew
    def crew(self) -> Crew:
        """Create and return the complete research crew.

        Returns:
            Crew: Configured crew with all agents and tasks in sequential process
        """
        return Crew(
            agents=[
                self.research_agent_method(),
                self.summarization_agent_method(),
                self.fact_checker_agent_method()
            ],
            tasks=[
                self.research_task_method(),
                self.summarization_task_method(),
                self.fact_checking_task_method()
            ],
            process=Process.sequential,
            verbose=True
        )

    # Convenience methods using original names
    def research_agent(self) -> Agent:
        """Get the research agent (convenience method).

        Returns:
            Agent: The research agent instance
        """
        return self.research_agent_method()

    def summarization_agent(self) -> Agent:
        """Get the summarization agent (convenience method).

        Returns:
            Agent: The summarization agent instance
        """
        return self.summarization_agent_method()

    def fact_checker_agent(self) -> Agent:
        """Get the fact-checking agent (convenience method).

        Returns:
            Agent: The fact-checking agent instance
        """
        return self.fact_checker_agent_method()

    def research_task(self) -> Task:
        """Get the research task (convenience method).

        Returns:
            Task: The research task instance
        """
        return self.research_task_method()

    def summarization_task(self) -> Task:
        """Get the summarization task (convenience method).

        Returns:
            Task: The summarization task instance
        """
        return self.summarization_task_method()

    def fact_checking_task(self) -> Task:
        """Get the fact-checking task (convenience method).

        Returns:
            Task: The fact-checking task instance
        """
        return self.fact_checking_task_method()

    # Helper methods to discover decorated methods
    def get_agents(self):
        """Get all methods decorated as agents.

        Returns:
            list: List of bound methods that are decorated as agents
        """
        return [getattr(self, name) for name in dir(self)
                if hasattr(getattr(self, name), '_is_agent')]

    def get_tasks(self):
        """Get all methods decorated as tasks.

        Returns:
            list: List of bound methods that are decorated as tasks
        """
        return [getattr(self, name) for name in dir(self)
                if hasattr(getattr(self, name), '_is_task')]

    def get_crew_builder(self):
        """Get the method decorated as crew builder.

        Returns:
            method or None: The bound method decorated as crew builder, 
                           or None if not found
        """
        for name in dir(self):
            method = getattr(self, name)
            if hasattr(method, '_is_crew'):
                return method
        return None
