Any developer should follow next rules to create Pull Requests.

***

### Commits

Commit naming rules are presented [in this page](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit-message-format).

Each commit should have not many differences excluding cases with:

  * CodeStyle changes;
  * Renames;
  * Code formatting.

**Do atomic commits for each change.** 
<pre>
refactor(class): correct indents before function params
refactor(class): rename vars according to codestyle
</pre>

**Don't mix codestyle changes and any logical fixes in one commit.**

***

_**All commit, that not applies to these rules, should be split by these rules. Another way they will be rejected with Pull request.**_
### Python pull requests rules

For each pull request you should check:

  * PEP8 code compliance
  * No commented out code
  * Names of classes, functions and variables should reflect the purpose
  * Use snake_case
  * Don't create new files for functions of the same class
  * Code compliance the Python style
  * Decompose tasks
  * Follow the DRY principle
