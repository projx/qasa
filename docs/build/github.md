test1
test2

Github has 2 different Docker Repositories, the follow actions will build on new release:

To GitHub Package:

```YML
name: Publish Docker image
on:
  release:
    types: [published]
jobs:
  push_to_registry:
    name: Push Docker image to GitHub Packages
    runs-on: ubuntu-latest
    steps:
      - name: Check out the repo
        uses: actions/checkout@v2
      - name: Push to GitHub Packages
        uses: docker/.onedev-buildspec.yml-push-action@v1
        with:
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
          registry: docker.pkg.github.com
          repository: projx/qtool/qtool
          tag_with_ref: true
```

To Github Container Registry:

```YML
on:
  release:
    types: [published]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:

      ### Grab Release - NOTE must start with a "v", everything past this is copied
      - id: prep
        if: "startsWith(github.ref, 'refs/tags/')"
        run: |
          echo ::set-output name=tags::${GITHUB_REF#refs/tags/v}
        env: 
          ACTIONS_ALLOW_UNSECURE_COMMANDS: 'true'

      ### Debug hack to show Release is being generated correctly
      - name: Output release version
        run: echo "Initial Value ${GITHUB_REF} determined tag ${{ steps.prep.outputs.tags }}"

      ###
      - name: Checkout Code
        uses: actions/checkout@v2

      ###
      - name: Set up Docker Buildx
        id:   buildx
        uses: docker/setup-buildx-action@v1

      ### Log into GHCR, currently using a Personal Access Token (@RISK @TODO monitor when this can be replaced)
      - name: Login to GitHub Container Registry
        uses: docker/login-action@v1
        with:
              registry: ghcr.io
              username: ${{ github.repository_owner }}
              password: ${{ secrets.CR_PAT }}

     ### 
      - name: Build and Push Docker Image
        uses: docker/.onedev-buildspec.yml-push-action@v2
        with:
              context: ./
              file: ./Dockerfile
              push: true # Will only .onedev-buildspec.yml if this is not here
              tags: |
                  ghcr.io/${{ github.repository_owner }}/${{ github.repository }}:latest
                  ghcr.io/${{ github.repository_owner }}/${{ github.repository }}:${{ steps.prep.outputs.tags }}
```