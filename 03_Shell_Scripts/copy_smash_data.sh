#!/usr/bin/env bash

# -----------------------------
# Pfadangaben (sollten eigentlich nicht mehr geändert werden)
# -----------------------------
# Alias des Remote-Servers wie in .ssh/config benannt
REMOTE_ALIAS="gsi-files"
# Basispfadangaben für remote und local
REMOTE_DATA_PATH="/lustre/hyihp/sostrows/smash_outputs"
LOCAL_TARGET="$HOME/dev/python/bachelor-thesis-physics/05_Files_from_Virgo"

# -----------------------------
# Steuerung (hier Ordnernamen anpassen)
# -----------------------------
# dry run flag: true -> nur anzeigen, false -> wirklich kopieren
DRY_RUN=false

# Mehrere Ordner: einfach Liste pflegen
FOLDERS_TO_COPY=(
  "Dilepton_Out_Std_Nevents_5_OutInt_NaN"
)

# -----------------------------
# rsync-Optionen (nur RSYNC_OPTS anpassen!)
# -----------------------------
RSYNC_OPTS="-avz --info=progress2"

# DO NOT TOUCH!
if [[ "$DRY_RUN" == true ]]; then
    RSYNC_OPTS="$RSYNC_OPTS --dry-run"
    echo "[DRY-RUN] Es werden keine Daten kopiert"
fi

# -----------------------------
# Loop über alle Ordner
# -----------------------------
for FOLDER_TO_COPY in "${FOLDERS_TO_COPY[@]}"; do
  COMPLETE_REMOTE_DIR="${REMOTE_ALIAS}:${REMOTE_DATA_PATH}/${FOLDER_TO_COPY}/"
  COMPLETE_LOCAL_DIR="${LOCAL_TARGET}/${FOLDER_TO_COPY}/"

  echo "------------------------------"
  echo "Prüfe Existenz des Remote-Ordners:"
  echo "  ${COMPLETE_REMOTE_DIR}"

  if ! ssh "$REMOTE_ALIAS" "[[ -d \"${REMOTE_DATA_PATH}/${FOLDER_TO_COPY}\" ]]"; then
    echo "WARNUNG: Remote-Ordner existiert nicht: ${REMOTE_DATA_PATH}/${FOLDER_TO_COPY}"
    echo "Weiter zum nächsten Ordner..."
    # Je nach Wunsch:
    # 1) weiter mit nächsten Ordner:
    continue
    # 2) oder hart abbrechen:
    # return 1 2>/dev/null || exit 1
  fi

  echo "Remote-Ordner gefunden"
  echo "Kopiere von: $COMPLETE_REMOTE_DIR"
  echo "Nach:        $COMPLETE_LOCAL_DIR"

  rsync $RSYNC_OPTS "$COMPLETE_REMOTE_DIR" "$COMPLETE_LOCAL_DIR"
done