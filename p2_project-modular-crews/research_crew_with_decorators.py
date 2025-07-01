"""Research crew implementation using official CrewAI decorators.

This module provides a ResearchCrew class that uses the official CrewAI 
@CrewBase, @agent, @task, and @crew decorators. This approach works well
in standalone Python files but may have limitations in Jupyter notebooks.
"""
from crewai import Agent, Crew, Task, Process
from crewai.project import CrewBase, agent, task, crew
from crewai_tools import SerperDevTool


@CrewBase
class ResearchCrew:
    """A crew for conducting research, summarizing findings, and fact-checking.

    This class uses the official CrewAI decorators to create a research workflow 
    with three specialized agents and their corresponding tasks.

    Attributes:
        agents_config (str): Path to the agents configuration YAML file
        tasks_config (str): Path to the tasks configuration YAML file
        search_tool (SerperDevTool): Tool for web-based research and fact-checking
    """

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        """Initialize the ResearchCrew with search tools."""
        self.search_tool = SerperDevTool()

    @agent
    def research_agent(self) -> Agent:
        """Create and return the research agent.

        Returns:
            Agent: Configured research agent with web search capabilities
        """
        return Agent(
            config=self.agents_config['research_agent'],  # pylint: disable=unsubscriptable-object
            tools=[self.search_tool],
            verbose=True
        )

    @agent
    def summarization_agent(self) -> Agent:
        """Create and return the summarization agent.

        Returns:
            Agent: Configured summarization agent for condensing research findings
        """
        return Agent(
            config=self.agents_config['summarization_agent'],  # pylint: disable=unsubscriptable-object
            verbose=True
        )

    @agent
    def fact_checker_agent(self) -> Agent:
        """Create and return the fact-checking agent.

        Returns:
            Agent: Configured fact-checking agent with web search capabilities
        """
        return Agent(
            config=self.agents_config['fact_checker_agent'],  # pylint: disable=unsubscriptable-object
            tools=[self.search_tool],
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        """Create and return the research task.

        Returns:
            Task: Configured task for conducting web-based research
        """
        return Task(
            config=self.tasks_config['research_task'],  # pylint: disable=unsubscriptable-object
            tools=[self.search_tool]
        )

    @task
    def summarization_task(self) -> Task:
        """Create and return the summarization task.

        Returns:
            Task: Configured task for summarizing research findings
        """
        return Task(
            config=self.tasks_config['summarization_task']  # pylint: disable=unsubscriptable-object
        )

    @task
    def fact_checking_task(self) -> Task:
        """Create and return the fact-checking task.

        Returns:
            Task: Configured task for validating information accuracy
        """
        return Task(
            config=self.tasks_config['fact_checking_task'],  # pylint: disable=unsubscriptable-object
            tools=[self.search_tool]
        )

    @crew
    def crew(self) -> Crew:
        """Create and return the complete research crew.

        Returns:
            Crew: Configured crew with all agents and tasks in sequential process
        """
        return Crew(
            agents=self.agents,  # pylint: disable=no-member
            tasks=self.tasks,    # pylint: disable=no-member
            process=Process.sequential,
            verbose=True
        )
