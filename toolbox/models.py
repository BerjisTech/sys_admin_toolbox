from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Tool(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Server(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                               related_name='children',
                               help_text="If this server is a child, link to a parent server.")
    name = models.CharField(max_length=200, help_text="Friendly name or label for the server.")
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, blank=True, null=True)
    endpoint = models.URLField(blank=True, null=True,
        help_text="For Amazon EC2 or other remote endpoints, store the URL here.")
    tools = models.ManyToManyField(Tool, blank=True,
        help_text="Tools like Elasticsearch, Docker, MySQL, etc.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ServerLog(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='logs')
    log_type = models.CharField(max_length=100, help_text="Type of the log e.g. 'Docker logs', 'Syslog', etc.")
    content = models.TextField(help_text="The actual log content.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.log_type} - {self.server.name}"
