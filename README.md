# toEaseShifts

The toEaseShifts application aims to make it easier for team managers to automatically generate staff scheduling by work shifts.

## Staging and Production Servers

Using Google Cloud - Cloud Computing we built 2 servers that are currently available:

[Staging Server](http://34.175.201.145/) automatically using the last commit on the dev branch.

[Production Server](http://34.175.53.246) automatically using the last commit on the master branch.

## How to contribute

In order to ensure the efficiency of our software development process, we enforce a variety of requirements, both stylistic and technological.

More details can be found in our [development guide](docs/development.md#development-guide).

### File/folder naming conventions

File and folder names in our backend application should be written in _snake_case_. In our frontend application, these should be written in camelCase, or PascalCase when named after a component.

### Commits, branches and pull requests

Commits must be accompanied by appropriate commit messages, which must follow the format `<type>(<scope>): <subject>` (scope is optional).

Branch names should follow the following format `<type>/<scope>/<subject>` (scope is optional).

The scope and subject must be written in _kebab-case_.

Pull requests should follow the same format as the commit messages, and follow the following rules:

-   body must contain a description of the changes made;
-   body must contain a link to the issue the pull request addresses;
-   should be reviewed by at least three other developers before being merged into the main branch (ideally, at least one from a different team);
-   in the case that pair/ensemble programming was done, it should be specified in the description of the pull request.

### Development dependencies and tools

Make sure you have version **14.17.0** or higher of node, as well as the `pip` and `npm` package managers installed on your system before following the next few steps.

To install the development dependencies for the project, run the following commands from the root directory:

```sh
python -m pip install -r backend/requirements_dev.txt
cd frontend && npm ci
```

In order to run the project's formatters:

```sh
cd backend
python -m black .
cd ../frontend
npx prettier --write ..
```

For the linters:

```sh
cd backend
python -m pylint --recursive=y .
cd ../frontend
npx eslint .
```

Setting up linter/formatter hooks:

```sh
git config --local core.hooksPath .githooks/
```

For running tests:

```sh
cd backend
python -m manage.py test
cd ../frontend
npm test
```

### Building and running the development application

In order to build, either:

-   navigate into the `backend` and `frontend` directories and run `docker build .`;
-   or run `docker-compose build` from the project's root directory

To run the project on a development environment, simply execute `docker-compose up` on the root directory.

To run a development version of the frontend application, supporting hot reloading, run `npm start` on the `frontend` directory.

The application should launch on `http://localhost:3000/`. PGAdmin can be accessed via `http://localhost:4321`.

## How to run

In order to run the service and pop up the website, we need to use the Google Cloud Services.

To **create an account** on the website you will need to introduce the information from a credit card. However, if you use the free/tryout plan you won’t be charged any fees.

Assuming this stage is clear, in the main screen you will find an option to **create a project**. After clicking there, you will be prompted to name your project and to conclude the creation process. You should wait a few seconds before the whole process sets up, so you can move to the next step.

After that, we need to **set the VPS (Virtual Private Server)**. On the sidebar, in the Computer Engine tab, we can find the ‘VM instances’ section. When creating the virtual machine there will be many options to configure it, like the name, region or the machine settings, so it’s up to you to select your preferences.

At this moment we can access the website, however, we don’t want to access it exclusively in google cloud all the time, so we have to **set a ‘ssh’ key**, if we don’t have any. You may do this by accessing your command line, and typing ‘ssh-keygen’, in your user folder. You may set more options for this command or seek help in this link: https://cloud.google.com/compute/docs/connect/create-ssh-keys#linux-and-macos.

To add it to the VM you need to grab the key from the ssh file you just created, and insert it in the edit instance menu (ssh key section).

The next part involves more commands. At this stage, we need to **set up the docker repository in our vps**. To do this, we need to open our VM’s command prompt, using the connect ‘ssh’ option in the same page as before. Afterwards, as in the development stage, we need to set docker for our repository using various commands. This guide is thoroughly explained for Ubuntu here: https://docs.docker.com/engine/install/ubuntu/.

Finally, the only thing remaining is **creating a firewall rule**. To do this, we need to go to the side bar and select, in the vm networks tab, the firewalls rule tab. The options we need to define in the creation settings are:

1. giving it a name and target tag,
2. setting the network as `vpc1`,
3. ‘Allow’ the action on match,
4. type the public internet ip: `0.0.0.0/0` on the source ips,
5. insert the tcp port: 80.

You can find more information about this in: https://cloud.google.com/vpc/docs/using-firewalls.
At last, you only need to go back to the instance page and add the firewall rule tag to the network tags.

Now, to **run the service** you need to clone this repository and execute the `docker-compose -f docker-compose.yml -f docker-compose.production.yml up --build -d` command. Our website will now be up and running at the external IP address of our VPS machine.
Assuming all steps went through without problems, the production environment should be working fine.

## Documentation

Documentation for the project is available in the [docs](docs/) directory. The following documents are available:

-   [Product](docs/product.md)
-   [Development](docs/development.md)
-   [User story template](docs/user_story_template.md)
-   [Factsheet template for contributors](docs/factsheet_contributor_template.md)
-   [Factsheet template for teams](docs/factsheet_team_template.md)
-   [Retrospectives](docs/development.md#restrospectives)
-   [REST API Specification](docs/api.yml)
-   [Demo Feedback](docs/demo_feedback.md)

## Contributions

-   [Team 1](factsheets/team1.md)

    -   [Adriano Soares](factsheets/adriano_soares.md) (SM)
    -   [André Santos](factsheets/andre_santos.md)
    -   [Eunice Amorim](factsheets/eunice_amorim.md) (SPO)
    -   [Joel Fernandes](factsheets/joel_fernandes.md)
    -   [Mário Travassos](factsheets/mario_travassos.md)
    -   [Pedro Correia](factsheets/pedro_correia.md)

-   [Team 2](factsheets/team2.md)

    -   [Fernando Rego](factsheets/fernando_rego.md)
    -   [Rodrigo Tuna](factsheets/rodrigo_tuna.md)
    -   [Rui Moreira](factsheets/rui_moreira.md)
    -   [Tiago Silva](factsheets/tiago_silva.md) (SPO)
    -   [Tiago Rodrigues](factsheets/tiago_rodrigues.md) (SM)
    -   [Vasco Gomes](factsheets/vasco_gomes.md)

-   [Team 3](factsheets/team3.md)

    -   [Beatriz Aguiar](factsheets/beatriz_aguiar.md) (SM)
    -   [Ângela Coelho](factsheets/angela_coelho.md)
    -   [Bruno Gomes](factsheets/bruno_gomes.md)
    -   [Filipe Campos](factsheets/filipe_campos.md)
    -   [João Marinho](factsheets/joao_marinho.md) (SPO)
    -   [Miguel Amorim](factsheets/miguel_amorim.md)

-   [Team 4](factsheets/team4.md)
    -   [André Pereira](factsheets/andre_pereira.md) (SPO)
    -   [Francisco Cerqueira](factsheets/francisco_cerqueira.md)
    -   [Henrique Sousa](factsheets/henrique_sousa.md) (SM)
    -   [Mafalda Magalhães](factsheets/mafalda_magalhaes.md)
    -   [Margarida Vieira](factsheets/margarida_vieira.md)
    -   [Rita Mendes](factsheets/rita_mendes.md)
