#/usr/bin/env bash
_mailadmin_completions()
{

  # Debug
  if [ "$COMPLETION_MAILADMIN" = "DEBUG" ]; then
  	echo ""
  	echo "Com: $COMP_WORDS ${COMP_WORDS[1]} ${COMP_WORDS[2]} ${#COMP_WORDS[@]}"
  	echo ""
  fi

  # Level 1
  if [ "${#COMP_WORDS[@]}" = "2" ]; then
  	COMPREPLY=($(compgen -W "list show add grant help" "${COMP_WORDS[1]}"))
  fi

  # Level 2
  if [ "${#COMP_WORDS[@]}" = "3" ] && [ "${COMP_WORDS[1]}" = "list" ]; then
    COMPREPLY=($(compgen -W "users domains addresses" "${COMP_WORDS[2]}"))
  fi

  if [ "${#COMP_WORDS[@]}" = "3" ] && [ "${COMP_WORDS[1]}" = "show" ]; then
    COMPREPLY=($(compgen -W "user domain address" "${COMP_WORDS[2]}"))
  fi

  if [ "${#COMP_WORDS[@]}" = "3" ] && [ "${COMP_WORDS[1]}" = "add" ]; then
    COMPREPLY=($(compgen -W "user domain address" "${COMP_WORDS[2]}"))
  fi

  if [ "${#COMP_WORDS[@]}" = "3" ] && [ "${COMP_WORDS[1]}" = "grant" ]; then
    COMPREPLY=($(compgen -W "domain address" "${COMP_WORDS[2]}"))
  fi

  # Level 4 in grant
  if [ "${#COMP_WORDS[@]}" = "5" ] && [ "${COMP_WORDS[1]}" = "grant" ]; then
    COMPREPLY=($(compgen -W "to" "${COMP_WORDS[4]}"))
  fi
}

complete -F _mailadmin_completions mailadmin