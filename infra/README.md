# Infrastructure

This README serves to document to myself what it is that I have learned about Terraform and Ansible, how I have used them in this project, and how I might use them in the future.
I am using Terraform to construct the AWS resources I'm using and using Ansible to manage and provision the servers.
I am not currently using anything specific to tie these two systems together, at the moment all configuration files are created and populated manually.

## Terraform

Terraform is an infrastructure as code software which allows us to create resources in the cloud in a reusable, code-based way.
Terraform uses a declarative language, whereby we write up a list of what we want created in the cloud, and Terraform creates it.

The project in question is a very simple one and so the Terraform code necessary is not much.
Did we have to use Terraform here? No, but I wanted the chance to try to get more familiar.
The infrastructure consists of a single EC2 instance and S3 bucket, and an instance profile that allows the instance to access the bucket.

I have yet to build in the elastic ip address and I would also like to add at "Do not destroy" to the S3 bucket.
I would like to better understand what it would look like to build this out for a multi machine setup. 
In a situation where there are two webservers, a load balancers and a database server, how is the networking configured?

### Protecting resources

It seems there is no great method in Terraform for protecting resources from destruction.
It's possible to add a lifecycle tag and use `prevent_destroy` or some such, but this just throws an error when tearing down.
I would like to have the S3 bucket and the Elastic IP kept from being destroyed. 
The S3 bucket will have content in it and so it won't be deleted.
But the IP address will. 
My thinking is that for all non-production uses of this code, no elastic ip address will be used; it will be skipped.
However, for prod use, I will merely attach the elastic IP address, which I will just have created manually.
Considerations:
I will need an if statements in the Terraform code, if prod (in variables?) then use IP address, if not then forget it.
I am going to leave this undone for now and proceed with assuming that we aren't going to use an elastic ip.

TODO: make greencover user able to spin this up

### References

[For booleans](https://blog.gruntwork.io/terraform-tips-tricks-loops-if-statements-and-gotchas-f739bbae55f9)
[This](https://www.youtube.com/watch?v=UleogrJkZn0) was a helpful example.
I haven't yet explored [this](https://github.com/28mm/awesome-terraform) but it seems to be a comprehensive list of resources.
Multiple server configuration [here](https://medium.com/@dhelios/terraform-by-examples-part-1-ef3e3be7b88b)
Useful for variable defintion and SSL certs [here](https://medium.com/modern-stack/5-minute-static-ssl-website-in-aws-with-terraform-76819a12d412)
[For different environments](https://betterprogramming.pub/managing-multiple-environments-in-terraform-5b389da3a2ef)


## Ansible

Ansible is a provisioning and configuration management software.
I am using this to do all the setup on the server. 
Since I'm on a single machine I could just use bash scripts and nest them inside a `remote-exec` tag in Terraform, but that seemed too boring.
To setup Ansible on Ubuntu, I ran the following to get the most up-to-date version:
```shell
sudo apt update
sudo apt install software-properties-common
sudo apt-add-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
# For postgres extensions
ansible-galaxy collection install community.general
ansible-galaxy collection install community.postgresql
```

I have setup the Ansible playbooks as if there is a database server as well as a web server, though its all on one for now. 
There are clever ways to have everything run through roles and so things can be executed with a single Ansible call, but I have not done that.
Right now, the db play must be run before the website because the website loads data to the database.
In the case where there are multiple webservers, there are several steps that would only need to be run on one of them.

A major todo I have is to manage the config files for Terraform and Ansible as well as for the Django project itself.
I think I may use `bash` for this but perhaps there is an easier and tidier solution somehwere.
Currently, I need to manually replace the web server's ip address and put it in the hosts file for Ansible as well as the `.env` file for the Django project. 
Similarly, the bucket name, AWS id and AWS secret key are in the `.env` file, the Terraform configs and the Ansible configs; something that needs tidying.

I need to look into Dynamic inventory.

### How to run

These ansible files require a file at `./ansible/vars/main.yml` which would look like this:
```yaml
---
database_user: db_user_name
database_name: database_name
database_pass: mycoolpassword
```

It also requires `./ansible/hosts` file, looking like:
`12.345.678.910 ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/sandbox1.pem`

Querying output variables
`ssh -i ~/.ssh/sandbox1.pem ubuntu@$(terraform output ip)`
`ssh -i ~/.ssh/sandbox1.pem ubuntu@$(terraform output el_pub_ip)`


`aws s3 cp ./test.txt s3://greencover-sandbox/test.txt`


### References

 - https://www.youtube.com/watch?v=UleogrJkZn0
 - [Cron job](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/cron_module.html)
 - [For Django and Ansible](https://realpython.com/automating-django-deployments-with-fabric-and-ansible/)
 - [Ansible loop](https://linuxhint.com/install_multiple_packages_centos_ansible/)
 - [Ansible examples](https://github.com/ansible/ansible-examples/tree/master/lamp_simple)
 - [Here](https://ansible.github.io/workshops/exercises/ansible_rhel/1.2-adhoc/) 
 - What the hell is `become`? [Check here](http://docs.ansible.com/ansible/latest/user_guide/become.html)


## Workflow

The bash script `helper.sh` is used to run Terraform and Ansible within one program.
It allows us maintain only one config file, the `.env` file, which is used by `decouple` within the Django application.
See the example file `.env.example` for what this should look like.
If you aren't going to use the default named environment file, `.env`, then specify the path to your env file with `-f ../test.env`.
Make sure that `DEPLOYED` is set to `True`.
The helper program first generates the Terraform and Ansible variable files using
`./helper.sh create_vars`.
Then, it calls the Terraform code, `./helper.sh spinup_infra`.
After this, provision and configure the infrastructure with Ansible using `./helper.sh deploy`.
Check to see if database and user are created:
```shell

sudo su - postgres
psql
# list databases
\l
# list tables
\dt
# list users (roles)
\du
```

For prod, manually dis and reassociated the elastic ip address to the new instance. 
Then run `terraform refresh`.
Then update `.env` with the new elastic ip and domain name and restart.
`ALLOWED_HOSTS=3.18.3.175,evansgeospatial.com,www.evansgeospatial.com`
### For local setup on new machine

0. Install ansible
1. Clone project
2. Create virtual env and activate
3. pip install requirements
4. Install postgres and run the following ansible

The Ansible scripts can be used to setup the software needed to run the website locally.
To install the necessary database software `./ansible/hosts` is not necessary, but the database playbook should have 

```yaml
- hosts: localhost
  connection: local
```
Otherwise it should look like
```yaml
- hosts: all
  remote_user: ubuntu
```

Then to install the software use:
`ansible-playbook ./ansible/database.yml --ask-become-pass`
On a local machine the user should also have createdb permissions to run tests.

`ALTER USER usr_davemike CREATEDB;`

In addition, one needs add the postgis extension the `template1` database so 
when this is copied it will have the extension present.

`psql -d template1`
`CREATE EXTENSION IF NOT EXISTS postgis;`

5. `python manage.py migrate`
 and then `python manage.py createsuperuser`


## Workspaces

`terraform workspace new dev`
# or 
`terraform workspace select dev`
# or 
`terraform workspace select default`

`terraform plan -out=tfdev_plan -var 'env=dev'`
`terraform apply tfdev_plan`

## For populating gdd and county for the first time

While in shell

```python
from kanopy.models import Groundcoverdoc

docs = Groundcoverdoc.objects.all()

for i, doc in enumerate(docs):
  print(i, "of", len(docs), ":", doc.location_name)
  print("  Before: " + str(doc.gdd))
  doc.populate_gdd()
  doc.populate_county()
  doc.save()
  print("  After: " + str(doc.gdd))
  print("  Cty: " + str(doc.county_name))
  
```

## Strange errors

### Invalid HTTP_HOST hearder

```[Wed Apr 19 11:32:56.516830 2023] [wsgi:error] [pid 20460:tid 140413916354304] [remote 45.159.208.76:43834] Invalid HTTP_HOST header: 'azenv.net'. You may need to add 'azenv.net' to ALLOWED_HOSTS.
```

[This](https://www.borfast.com/blog/2020/07/06/invalid-http_host-header-errors-in-django-and-nginx/) article and [this one](https://www.untangled.dev/2020/07/07/invalid-http-host-header-barrage/) explains a strange error I've been getting.
The headers vary widely but apparently these are hacking attempts. 
The article explains how to configure Nginx to deal with this better but not sure about Apache.

Seen this with `tail /var/log/apache2/error.log`

Will wait to see error again but will try [this solution](https://stackoverflow.com/questions/39513109/django-invalid-http-host-header-on-apache-fix-using-require) next.


### Multiple interpreters?

```[Wed Apr 19 13:32:53.165614 2023] [wsgi:error] [pid 20767:tid 140194198103808] [remote 5.226.139.17:63031]     from .gdd_calc import calc_gdd```

```[Wed Apr 19 13:32:53.165739 2023] [wsgi:error] [pid 20767:tid 140194198103808] [remote 5.226.139.17:63031] ImportError: Interpreter change detected - this module can only be loaded into one interpreter per process.```

```[Mon Apr 17 20:57:16.534248 2023] [wsgi:error] [pid 16301:tid 140292409382656] /home/ubuntu/exploring_soils/myvenv/lib/python3.8/site-packages/django/contrib/gis/shortcuts.py:10: UserWarning: NumPy was imported from a Python sub-interpreter but NumPy does not properly support sub-interpreters. This will likely work for most users but might cause hard to track down issues or subtle bugs. A common user of the rare sub-interpreter feature is wsgi which also allows single-interpreter mode.
[Mon Apr 17 20:57:16.534856 2023] [wsgi:error] [pid 16301:tid 140292409382656] Improvements in the case of bugs are welcome, but is not on the NumPy roadmap, and full support may require significant effort to achieve.```


## Moving to Nginx and Gunicorn

Following [this website](https://www.agiliq.com/blog/2013/08/minimal-nginx-and-gunicorn-configuration-for-djang/)

for development use the following rather than `python manage.py runserver` 
`gunicorn exploring_soils.wsgi:application`
or `gunicorn exploring_soils.wsgi:application --bind=127.0.0.1:8001`

This won't service static content so need to put each subdirectory of 

Also maybe below is good.
http://www.alirazabhayani.com/2013/02/easy-django-deployment-tools-tutorial-fabric-gunicorn-nginx-supervisor.html

https://faun.pub/deploy-django-app-with-nginx-gunicorn-and-supervisor-on-ubuntu-server-ff58f5c201ac

#### For switching between Test and Prod

 - update terraform workspace (`terraform workspace select <tier>`)
 - change `.env` file (`cp <tier>.env .env`)
 - check git branch
 - If remote instance already exists, then update ansible hosts file

 - Apply elastic IP
 - Refresh IP in terraform with `terraform refresh`
 - update ssh key
 - update remote instance of .env with new elastic ip and domain name (e.g. `ALLOWED_HOSTS=3.18.3.175,evansgeospatial.com,www.evansgeospatial.com`) and update `CSRF_TRUSTED_ORIGINS` with <tier>.evansgeospatial.com and restart 


#### Miscellaneous 

 Error: https://stackoverflow.com/questions/65025278/apache2-django-nameerror-name-typeerror-is-not-defined


