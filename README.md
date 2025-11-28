=== TO-DO LIST APP ===

HVA PROGRAMMET GJØR:
------------------------------------------------------------------------
Programmet er en oppgavebehandler med grafisk brukergrensesnitt.

Det har følgende hovedfunksjoner:
1. **Legge til oppgaver** – opprette nye oppgaver med valgt prioritet (Høy, Medium, Lav);
2. **Administrere oppgaver** – markere som fullført, redigere og slette oppgaver;
3. **Lagre data** – automatisk lagring av oppgaver mellom økter (og manuelt via knapp);
4. **Eksportere oppgaver** – mulighet til å eksportere oppgavelisten til en tekstfil;

HVORDAN DET BRUKES:
------------------------------------------------------------------------
1. Start programmet ved å kjøre "main.py";

2. For å legge til en ny oppgave:
    - Skriv inn oppgavens navn i tekstfeltet
    - Velg prioritet fra nedtrekksmenyen (standard er medium)
    - Trykk på "Add Task"

3. For å administrere eksisterende oppgaver:
    - Velg en oppgave i listen
    - Bruk knappene "Toggle Complete", "Edit", "Delete" for ønsket handling

4. For å eksportere oppgaver, trykk på "Export"

EVENTUELLE INSTALLASJONSKRAV:
------------------------------------------------------------------------
- Python 3.8 eller nyere;
- Tkinter (inkludert i standard Python-installasjon);
- Standard Python-biblioteker: json, datetime;

ENDRINGER SAMMENLIGNET MED DEN OPPRINNELIGE PLANEN:
------------------------------------------------------------------------
- Funksjonen for å eksportere oppgaver til en tekstfil ble lagt til, selv om den ikke var planlagt;
- Statistikken vises nå i den eksporterte TXT-filen, selv om det først var planlagt å vise den direkte i programmet;
- Følgende funksjoner ble ikke implementert: søk etter oppgaver, filter for visning av oppgaver, tillegg av deadline;

FORSLAG TIL VIDEREUTVIKLING:
------------------------------------------------------------------------
- Implementere alle tidligere planlagte funksjoner: oppgavesøk, filtrering, deadline for oppgaver;
- Legge til kategorier eller tags for oppgaver;
- Integrere statistikk og produktivitetsgrafer direkte i programmet;
- Implementere varslings- og påminnelsessystem;
- Legge til sortering av oppgaver etter forskjellige kriterier (prioritet, dato opprettet, aktive, fullførte osv.);
