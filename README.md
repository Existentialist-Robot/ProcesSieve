# ProcesSieve
Agile ideation, instantiation, iteration on business processes.

## Scope and Purpose

ProcesSieve is an agile, open framework designed to revolutionize how we ideate, instantiate, and iterate on business processes. Inspired by the collaborative spirit of the Enlightenment and the urgent need for decentralized, sustainable institutions, ProcesSieve empowers individuals and communities to build coordinated, impactful initiatives at scale.

Our platform reduces the friction of turning ideas into action by guiding users through three simple steps: ideation, instantiation, and iteration. Using AI-driven agents, ProcesSieve helps you refine your vision, build purpose-driven organizations, and generate strategic plans, KPIs, and SOPs tailored to your goals. It leverages narratives from real-world businesses to identify pain points and optimize processes, ensuring efficiency and scalability.

The AI is not there to give its own solutions, but to help you reason about your own practice in an agile manner, and to build a common of tested best practices that everybody can learn from.

Whether you’re an entrepreneur, community organizer, or innovator, ProcesSieve is a comprehensive tool that can help create sustainable, integrated advice and actions as solutions to business challenges. By fostering collaboration within and across disciplines and challenging outdated systems, we’re building a future where collective action drives meaningful change. Join us in reimagining institutions and unlocking the potential of decentralized, coordinated innovation.

## Setup

### Local 
From fresh OS, install the following system-level applications
- neo4j
- git
- visual code
- uv

uv sync --all-extras

### Cloud Integrations

Configure Cohere Private Key and input into a copy of the config.ini.template (saving it as config.ini)

Configure Cloud Drive integration

 - From Google Console (https://console.cloud.google.com/) - Create a Project
 - From IAM → Service Accounts - Create a Service Account with Edit Permissions 
 - Add the Service Account email to Target Drive (via sharing - can be done programmatically)
 - Create a Private Key for the Service Account
 - Download service-account.json and add to project root
 - Enable APIs for both Google Docs and Google Drive
