findscu -v -P \
  -k "QueryRetrieveLevel=WORKLIST" \
  -k "(0008,0060)=CT" \
  192.168.110.41 4242

  findscu -W -k "ScheduledProcedureStepSequence[0].Modality=US" -k "PatientName" -k "PatientID" -k "AccessionNumber" -k "StudyInstanceUID" -aec PACS 192.168.119.168 4242

[orthanc-wl-generate-example](https://orthanc.uclouvain.be/hg/orthanc/file/default/OrthancServer/Plugins/Samples/ModalityWorklists/WorklistsDatabase/) 

[orthanc wl docs](https://orthanc.uclouvain.be/book/plugins/worklists-plugin.html) 

```mwl
# Dicom-File-Format

# Dicom-Meta-Information-Header
(0002,0000) UL 202                                        # FileMetaInformationGroupLength
(0002,0001) OB 00\01                                     # FileMetaInformationVersion
(0002,0002) UI [MediaStorageSOPClassUID] # MediaStorageSOPClassUID
(0002,0003) UI [1.2.276.0.7230010.3.1.4.2831176407.11154.1448031138.805061] # MediaStorageSOPInstanceUID
(0002,0010) UI =LittleEndianExplicit                     # TransferSyntaxUID
(0002,0012) UI [1.2.276.0.7230010.3.0.3.6.0]             # ImplementationClassUID
(0002,0013) SH [OFFIS_DCMTK_360]                         # ImplementationVersionName

# Dicom-Data-Set
(0008,0005) CS [ISO_IR 100]                  # SpecificCharacterSet
(0008,0050) SH [AccessionNumber]          # AccessionNumber
(0008,0060) CS [Modality]                 # Modality
(0010,0010) PN [PatientName]              # PatientName
(0010,0020) LO [PatientID]                # PatientID
(0010,0030) DA [PatientBirthDate]         # PatientBirthDate
(0010,0040) CS [PatientSex]               # PatientSex
(0010,2000) LO [MedicalAlerts]            # MedicalAlerts
(0010,2110) LO [Allergies]                # Allergies
(0010,21B0) LT [AdditionalPatientHistory] # AdditionalPatientHistory
(0020,000d) UI [StudyInstanceUID]         # StudyInstanceUID
(0032,1032) PN [RequestingPhysician]      # RequestingPhysician
(0032,1060) LO [RequestedProcedureDescription]        #  RequestedProcedureDescription
(0040,0001) AE [ScheduleStationAETitle]               #  ScheduleStationAETitle
(0040,0002) DA [ScheduledProcedureStepStartDate]      #  ScheduledProcedureStepStartDate
(0040,0003) TM [ScheduledProcedureStepStartTime]      #  ScheduledProcedureStepStartTime
(0040,1001) SH [RequestedProcedureID]                 # RequestedProcedureID
(0040,1003) SH [RequestedProcedurePriority]           # RequestedProcedurePriority


```

```mwl
# Dicom-File-Format

# Dicom-Meta-Information-Header
(0002,0001) OB 00\01
(0002,0002) UI [1.2.840.10008.5.1.4.31]
(0002,0003) UI [1.2.826.0.1.3680043.2.1125.1762751716.1]
(0002,0010) UI =LittleEndianExplicit
(0002,0012) UI [1.2.276.0.7230010.3.0.3.6.0]
(0002,0013) SH [OFFIS_DCMTK_360]

# Dicom-Data-Set
(0008,0005) CS [ISO_IR 100]
(0008,0050) SH [8-01010]
(0008,0060) CS [CR]
(0010,0010) PN [jarwo]
(0010,0020) LO [010103]
(0020,000D) UI [1.2.826.0.1.3680043.2.1125.1762751716]
(0032,1032) PN [dokter radio]
(0032,1060) LO [01010]

(0040,0100) SQ (Sequence with explicit length #=1)
  (fffe,e000) na (Item with explicit length #=5)
    (0008,0060) CS [CR]
    (0040,0001) AE [CR]
    (0040,0002) DA [20250128]
    (0040,0003) TM [000000]
    (0040,1001) SH [8-01010]
  (fffe,e00d) na (ItemDelimitationItem)
(fffe,e0dd) na (SequenceDelimitationItem)

```
