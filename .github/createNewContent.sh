REPOSITORY_FOLDER="test-cms"

main () {
    configPaths
    
    configGit
    
    authenticateOnGithub
    
    changeBranch
    
    createDefaultContentStructure
    
    commitChanges
    
}

configPaths () {
    REPOSITORY_ABS_PATH="$(pwd)/$REPOSITORY_FOLDER"
    REPOSITORY_NEW_BRANCH="new-content-$CONTENT_PATH-$(date +%s)"
}

authenticateOnGithub () {
    echo -e "$GITHUB_TOKEN" > key.t
    unset GITHUB_TOKEN
    gh auth login --with-token < key.t
    rm key.t
    gh auth status
}

configGit() {
    git config --global user.name "$TRIGGERING_AUTHOR"
}

changeBranch() {
    echo "Changing branch"

    cd "$REPOSITORY_ABS_PATH" || exit
    git checkout -b "$REPOSITORY_NEW_BRANCH"
    
    echo "Branch name is $REPOSITORY_NEW_BRANCH"
}

createDefaultContentStructure() {
  cd "$REPOSITORY_ABS_PATH" || exit
  mkdir -p "$CONTENT_PATH/en"
  touch "$CONTENT_PATH/metadata.yml"
  touch "$CONTENT_PATH/en/en.md"
  echo "Your default English content in this file" >> "$CONTENT_PATH/en/en.md"
}

commitChanges() {
  cd "$REPOSITORY_ABS_PATH" || exit
  git add "$CONTENT_PATH"
  git commit -m "$REPOSITORY_NEW_BRANCH"
  git push -f --set-upstream origin "$REPOSITORY_NEW_BRANCH"
}

createPr() {
  cd "$REPOSITORY_ABS_PATH" || exit
  linkToTargetPR="$(gh pr create --title "Create new content for path $CONTENT_PATH" --base main --body "This PR is created from workflow")"
  echo "PR link $linkToTargetPR"
}

set -ex
main

