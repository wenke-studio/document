from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import Client
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.vcs import Gitlab


class GitLab:
    """GitLab architecture diagram

    Ref: https://docs.gitlab.com/ee/development/architecture.html
    """

    def __init__(self, filename: Path) -> None:
        with Diagram(str(filename), show=False, direction="TB"):
            with Cluster("Endpoints"):
                http = Client("HTTP/HTTPS")
                ssh = Client("SSH")

            nginx, gitlab_shell = self.create_core_layer()
            self.create_monitoring_layer()

            http >> nginx
            ssh >> gitlab_shell

    def create_core_layer(self):
        with Cluster("Core Processors Layer"):
            with Cluster("Interfaces"):
                nginx = Nginx("Proxy")
                gitlab_shell = Gitlab("GitLab Shell")

            with Cluster("Main"):
                gitlab_pages = Gitlab("GitLab Pages")
                gitlab_workhorse = Gitlab("GitLab Workhorse")
                sidekiq = Gitlab("Sidekiq (GitLab Rails)")
                puma = Gitlab("Puma (GitLab Rails)")

        with Cluster("Core Data Layer"):
            redis = Redis("Redis")
            postgresql = PostgreSQL("PostgreSQL")
            gitaly = Gitlab("Gitaly")

        nginx >> Edge(label="TCP :8090") >> gitlab_pages
        nginx >> gitlab_workhorse
        gitlab_shell >> [gitlab_workhorse, gitaly]

        gitlab_workhorse >> [redis, gitaly]

        sidekiq >> [redis, postgresql]
        puma >> [redis, postgresql, gitaly]

        gitaly >> gitlab_workhorse

        return nginx, gitlab_shell

    def create_monitoring_layer(self):
        pass
