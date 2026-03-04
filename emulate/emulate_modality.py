from time import sleep
from pydicom.dataset import Dataset
from pydicom import dcmread
from pynetdicom import AE
from pynetdicom.sop_class import ModalityWorklistInformationFind, DigitalXRayImageStorageForPresentation, ComputedRadiographyImageStorage
from pydicom.uid import ExplicitVRLittleEndian, ImplicitVRLittleEndian
import subprocess

ORTHANC_AE = 'PACS'
ORTHANC_IP = '192.168.110.41'
ORTHANC_PORT = 4242
DICOM_FILE = 'sample.dcm'  # pastikan file ini benar-benar uncompressed

# ----------------------------
# Buat Application Entity
# ----------------------------
ae = AE(ae_title='EMULATOR')
ae.add_requested_context(ModalityWorklistInformationFind)
ae.add_requested_context(
    # DigitalXRayImageStorageForPresentation,
    ComputedRadiographyImageStorage,
    [ExplicitVRLittleEndian, ImplicitVRLittleEndian]
)

# ----------------------------
# Query Worklist
# ----------------------------
ds = Dataset()
ds.Modality = 'CR'
ds.PatientName = ''
ds.PatientID = ''
ds.AccessionNumber = ''
ds.StudyInstanceUID = ''

assoc = ae.associate(ORTHANC_IP, ORTHANC_PORT, ae_title=ORTHANC_AE)
worklist_entries = []
if assoc.is_established:
    responses = assoc.send_c_find(ds, query_model=ModalityWorklistInformationFind)
    for status, identifier in responses:
        if status and status.Status in (0xFF00, 0xFF01):
            worklist_entries.append(identifier)
            print("Found Worklist Entry:", identifier)
    assoc.release()
else:
    print("Association failed!")
    exit(1)

if not worklist_entries:
    print("No Worklist entries found, exiting.")
    exit(1)

entry = worklist_entries[0]

print(entry)

# ----------------------------
# C-STORE DICOM
# ----------------------------
ds_file = dcmread(DICOM_FILE)
print('before edited')
print(ds_file) 

ds_file.decompress()   # <-- otomatis decompress kalau handler tersedia
ds_file.save_as("sample_unc.dcm")

from pydicom.uid import generate_uid
from datetime import datetime, time

ds_file = dcmread("sample_unc.dcm")

# Update metadata
ds_file.PatientName = entry.PatientName
ds_file.PatientID = entry.PatientID
ds_file.AccessionNumber = entry.AccessionNumber
ds_file.StudyInstanceUID = entry.StudyInstanceUID
ds_file.Modality = entry.ScheduledProcedureStepSequence[0].Modality if 'ScheduledProcedureStepSequence' in entry else 'CR'
ds_file.SeriesInstanceUID = generate_uid()
ds_file.SOPInstanceUID = generate_uid()
ds_file.SeriesNumber = 1
ds_file.InstanceNumber = 1
ds_file.StudyDate = datetime.now().strftime('%Y%m%d')
ds_file.StudyTime = datetime.now().strftime('%H%M%S')

# Update file meta
ds_file.file_meta.MediaStorageSOPClassUID = ds_file.SOPClassUID
ds_file.file_meta.MediaStorageSOPInstanceUID = ds_file.SOPInstanceUID
ds_file.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
ds_file.is_little_endian = True
ds_file.is_implicit_VR = False

# from pydicom.uid import RLELossless
# ds_file.compress(RLELossless)

ds_file.save_as("sample_edited_lossless.dcm")

print('\nafter edited\n')

ds_file_edited = dcmread("sample_edited_lossless.dcm")
print(ds_file_edited)

sleep(5)

filepath = '/mnt/dataD/backup/backup_windows/dgcell/P/experimental/github/pacs-lite/example/emulate/sample_edited_lossless.dcm'

command = [
    '/usr/bin/storescu',
    '--call', 'PACS',
    '192.168.110.41', '4242',
    filepath
]
try:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    print("Success:", result.stdout)
except subprocess.CalledProcessError as e:
    print("Error:", e.stderr)

# assoc = ae.associate(ORTHANC_IP, ORTHANC_PORT, ae_title=ORTHANC_AE)
# if assoc.is_established:
#     status = assoc.send_c_store(ds_file_edited)
#     if status:
#         print(f"C-STORE succeeded: 0x{status.Status:04x}")
#     assoc.release()
# else:
#     print("C-STORE association failed!")
#
