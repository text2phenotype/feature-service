code_relax = """
00000-0|Hospital Radiology
00000-0|Hospital Radiology
"""

code_strict = """
24754-4|Administration of vasodilator into catheter of Vein
26376-4|Administration of vasodilator into catheter of Vein - bilateral
26377-2|Administration of vasodilator into catheter of Vein - left
26378-0|Administration of vasodilator into catheter of Vein - right
30649-8|Peripheral artery Fluoroscopic angiogram Additional angioplasty W contrast IA
30641-5|Vein Fluoroscopic angiogram Additional angioplasty W contrast IV
36760-7|AV shunt Fluoroscopic angiogram Angioplasty W contrast
36762-3|Extremity vessel Fluoroscopic angiogram Angioplasty W contrast
69067-7|Unspecified body region Fluoroscopic angiogram Angioplasty W contrast
24543-1|Aorta Fluoroscopic angiogram Angioplasty W contrast IA
24580-3|Brachiocephalic artery Fluoroscopic angiogram Angioplasty W contrast IA
26368-1|Brachiocephalic artery - left Fluoroscopic angiogram Angioplasty W contrast IA
26369-9|Brachiocephalic artery - right Fluoroscopic angiogram Angioplasty W contrast IA
24614-0|Carotid artery extracranial Fluoroscopic angiogram Angioplasty W contrast IA
24615-7|Carotid artery intracranial Fluoroscopic angiogram Angioplasty W contrast IA
35881-2|Extremity artery Fluoroscopic angiogram Angioplasty W contrast IA
24698-3|Femoral artery Fluoroscopic angiogram Angioplasty W contrast IA
36763-1|Femoral artery and Popliteal artery Fluoroscopic angiogram Angioplasty W contrast IA
24766-8|Iliac artery Fluoroscopic angiogram Angioplasty W contrast IA
26370-7|Iliac artery - bilateral Fluoroscopic angiogram Angioplasty W contrast IA
26371-5|Iliac artery - left Fluoroscopic angiogram Angioplasty W contrast IA
26372-3|Iliac artery - right Fluoroscopic angiogram Angioplasty W contrast IA
24832-8|Mesenteric artery Fluoroscopic angiogram Angioplasty W contrast IA
30648-0|Peripheral artery Fluoroscopic angiogram Angioplasty W contrast IA
25081-1|Renal vessel Fluoroscopic angiogram Angioplasty W contrast IA
25012-6|Tibial artery Fluoroscopic angiogram Angioplasty W contrast IA
26373-1|Tibial artery - bilateral Fluoroscopic angiogram Angioplasty W contrast IA
26374-9|Tibial artery - left Fluoroscopic angiogram Angioplasty W contrast IA
26375-6|Tibial artery - right Fluoroscopic angiogram Angioplasty W contrast IA
43793-9|Tibioperoneal arteries Fluoroscopic angiogram Angioplasty W contrast IA
43794-7|Tibioperoneal arteries - bilateral Fluoroscopic angiogram Angioplasty W contrast IA
43795-4|Tibioperoneal arteries - left Fluoroscopic angiogram Angioplasty W contrast IA
43792-1|Tibioperoneal arteries - right Fluoroscopic angiogram Angioplasty W contrast IA
25064-7|Vessel Fluoroscopic angiogram Angioplasty W contrast IA
30836-1|Visceral artery Fluoroscopic angiogram Angioplasty W contrast IA
37426-4|Lower extremity vein Fluoroscopic angiogram Angioplasty W contrast IV
30640-7|Vein Fluoroscopic angiogram Angioplasty W contrast IV
35882-0|Inferior vena cava Fluoroscopic angiogram Angioplasty W contrast IV
36764-9|Femoral vessel and Popliteal artery Fluoroscopic angiogram Atherectomy W contrast
69135-2|Iliac artery Fluoroscopic angiogram Atherectomy W contrast
69253-3|Renal vessels Fluoroscopic angiogram Atherectomy W contrast
36765-6|Vessel Fluoroscopic angiogram Atherectomy W contrast
35883-8|Aorta Fluoroscopic angiogram Atherectomy W contrast IA
36766-4|Coronary arteries Fluoroscopic angiogram Atherectomy W contrast IA
24568-8|AV fistula Fluoroscopic angiogram Atherectomy W contrast IV
36761-5|Biliary ducts Fluoroscopy Balloon dilatation W contrast
38268-9|Skeletal system DXA Bone density
43562-8|Skeletal system.axial Scan Bone density
43563-6|Skeletal system.peripheral Scan Bone density
24631-4|Unspecified body region Fluoroscopy Central vein catheter placement check
25062-1|Unspecified body region X-ray Comparison view
72555-6|Interventional radiology Consult note
25038-1|Unspecified body region Courtesy consultation
24684-3|Extracranial vessels Fluoroscopic angiogram Embolectomy W contrast IA
24887-2|Pulmonary artery Fluoroscopic angiogram Embolectomy W contrast IA
24553-0|Vessel intracranial Fluoroscopic angiogram Embolectomy W contrast IV
24554-8|Artery Fluoroscopic angiogram Embolization W contrast IA
30600-1|Small bowel CT Views Enteroclysis W contrast PO via duodenal intubation
24923-5|Small bowel Fluoroscopy Views Enteroclysis W contrast PO via duodenal intubation
46365-3|CT Guidance for ablation of tissue of Celiac plexus
44228-5|CT Guidance for ablation of tissue of Kidney
44156-8|US Guidance for ablation of tissue of Kidney
44101-4|CT Guidance for ablation of tissue of Liver
44155-0|US Guidance for ablation of tissue of Liver
58747-7|CT Guidance for ablation of tissue of Unspecified body region
58743-6|US Guidance for ablation of tissue of Unspecified body region
35884-6|CT Guidance for abscess drainage of Abdomen
42280-8|CT Guidance for abscess drainage of Appendix
42705-4|US Guidance for abscess drainage of Appendix
42281-6|CT Guidance for abscess drainage of Chest
42285-7|CT Guidance for abscess drainage of Kidney
44167-5|US Guidance for abscess drainage of Kidney
42282-4|CT Guidance for abscess drainage of Liver
42133-9|US Guidance for abscess drainage of Liver
39361-1|Fluoroscopy Guidance for abscess drainage of Liver
69120-4|Fluoroscopy Guidance for abscess drainage of Neck
69122-0|Fluoroscopy Guidance for abscess drainage of Pancreas
42286-5|CT Guidance for abscess drainage of Pelvis
44168-3|US Guidance for abscess drainage of Pelvis
44169-1|US Guidance for abscess drainage of Peritoneal space
42284-0|CT Guidance for abscess drainage of Pleural space
69123-8|Fluoroscopy Guidance for abscess drainage of Pleural space
43502-4|CT Guidance for abscess drainage of Subphrenic space
44166-7|US Guidance for abscess drainage of Subphrenic space
30578-9|CT Guidance for abscess drainage of Unspecified body region
39451-0|US Guidance for abscess drainage of Unspecified body region
35885-3|Fluoroscopy Guidance for abscess drainage of Unspecified body region
39620-0|Scan Guidance for abscess localization limited
39623-4|Scan Guidance for abscess localization whole body
39622-6|SPECT Guidance for abscess localization whole body
39621-8|SPECT Guidance for abscess localization
72533-3|US Guidance for ambulatory phlebectomy of Extremity vein - left
72532-5|US Guidance for ambulatory phlebectomy of Extremity vein - right
24623-1|CT Guidance for anesthetic block injection of Celiac plexus
35886-1|CT Guidance for aspiration of Breast
24598-5|Mammogram Guidance for aspiration of Breast
43756-6|US Guidance for aspiration of Breast
69278-0|US Guidance for aspiration of Breast - bilateral
69292-1|US Guidance for aspiration of Breast - left
69296-2|US Guidance for aspiration of Breast - right
35888-7|Fluoroscopy Guidance for aspiration of Hip
24771-8|Fluoroscopy Guidance for aspiration of Joint space
48434-5|US Guidance for aspiration of Kidney
24811-2|CT Guidance for aspiration of Liver
24822-9|CT Guidance for aspiration of Lung
69287-1|US Guidance for aspiration of Lymph node
24837-7|CT Guidance for aspiration of Neck
39452-8|US Guidance for aspiration of Ovary
24856-7|CT Guidance for aspiration of Pancreas
24863-3|CT Guidance for aspiration of Pelvis
30703-3|US Guidance for aspiration of Pericardial space
37491-8|CT Guidance for aspiration of Pleural space
24662-9|US Guidance for aspiration of Pleural space
37887-7|Fluoroscopy Guidance for aspiration of Pleural space
24973-0|Fluoroscopy Guidance for aspiration of Spine Lumbar Space
42134-7|US Guidance for aspiration of Thyroid
25043-1|CT Guidance for aspiration of Unspecified body region
30878-3|US Guidance for aspiration of Unspecified body region
36926-4|CT Guidance for aspiration and placement of drainage tube of Abdomen
37210-2|CT Guidance for aspiration of cyst of Abdomen
69306-9|Fluoroscopy Guidance for aspiration of cyst of Bone
24594-4|Mammogram Guidance for aspiration of cyst of Breast
69192-3|MRI Guidance for aspiration of cyst of Breast
30653-0|US Guidance for aspiration of cyst of Breast
26343-4|Mammogram Guidance for aspiration of cyst of Breast - bilateral
38012-1|US Guidance for aspiration of cyst of Breast - bilateral
26344-2|Mammogram Guidance for aspiration of cyst of Breast - left
42450-7|US Guidance for aspiration of cyst of Breast - left
26345-9|Mammogram Guidance for aspiration of cyst of Breast - right
42458-0|US Guidance for aspiration of cyst of Breast - right
38126-9|US Guidance for aspiration of cyst of Kidney
69121-2|Fluoroscopy Guidance for aspiration of cyst of Ovary
38133-5|US Guidance for aspiration of cyst of Pancreas
42447-3|US Guidance for aspiration of cyst of Thyroid
35887-9|CT Guidance for aspiration of cyst of Unspecified body region
30698-5|US Guidance for aspiration of cyst of Unspecified body region
24671-0|Fluoroscopy Guidance for aspiration of cyst of Unspecified body region
25042-3|CT Guidance for aspiration or biopsy of Unspecified body region
25041-5|CT Guidance for aspiration or biopsy of Unspecified body region-- W contrast IV
46281-2|CT Guidance for aspiration or injection of cyst of Unspecified body region
46282-0|US Guidance for aspiration or injection of cyst of Unspecified body region
30602-7|CT Guidance for fine needle aspiration of Abdomen
44107-1|CT Guidance for fine needle aspiration of Abdomen retroperitoneum
44108-9|CT Guidance for fine needle aspiration of Adrenal gland
46387-7|Mammogram Guidance for fine needle aspiration of Breast
44160-0|US Guidance for fine needle aspiration of Breast
46284-6|Mammogram Guidance for fine needle aspiration of Breast - left
38026-1|US Guidance for fine needle aspiration of Breast - left
46283-8|Mammogram Guidance for fine needle aspiration of Breast - right
38033-7|US Guidance for fine needle aspiration of Breast - right
38135-0|US Guidance for fine needle aspiration of Deep tissue
44221-0|Fluoroscopy Guidance for fine needle aspiration of Deep tissue
43757-4|CT Guidance for fine needle aspiration of Kidney
44159-2|US Guidance for fine needle aspiration of Kidney
44217-8|Fluoroscopy Guidance for fine needle aspiration of Kidney
30608-4|CT Guidance for fine needle aspiration of Kidney - bilateral
30603-5|CT Guidance for fine needle aspiration of Liver
44158-4|US Guidance for fine needle aspiration of Liver
44220-2|Fluoroscopy Guidance for fine needle aspiration of Liver
30595-3|CT Guidance for fine needle aspiration of Lung
44103-0|CT Guidance for fine needle aspiration of Lymph node
44219-4|Fluoroscopy Guidance for fine needle aspiration of Lymph node
44104-8|CT Guidance for fine needle aspiration of Mediastinum
44105-5|CT Guidance for fine needle aspiration of Muscle
30605-0|CT Guidance for fine needle aspiration of Pancreas
44157-6|US Guidance for fine needle aspiration of Pancreas
44218-6|Fluoroscopy Guidance for fine needle aspiration of Pancreas
30606-8|CT Guidance for fine needle aspiration of Pelvis
44106-3|CT Guidance for fine needle aspiration of Prostate
38017-0|US Guidance for fine needle aspiration of Prostate
30610-0|CT Guidance for fine needle aspiration of Spleen
38136-8|US Guidance for fine needle aspiration of Superficial tissue
69124-6|Fluoroscopy Guidance for fine needle aspiration of Superficial tissue
38019-6|US Guidance for fine needle aspiration of Thyroid
44216-0|Fluoroscopy Guidance for fine needle aspiration of Thyroid
30580-5|CT Guidance for fine needle aspiration of Unspecified body region
38018-8|US Guidance for fine needle aspiration of Unspecified body region
44215-2|Fluoroscopy Guidance for fine needle aspiration of Unspecified body region
24755-1|Fluoroscopic angiogram Guidance for atherectomy of Vein-- W contrast IV
26298-0|Fluoroscopic angiogram Guidance for atherectomy of Vein - bilateral-- W contrast IV
26299-8|Fluoroscopic angiogram Guidance for atherectomy of Vein - left-- W contrast IV
26300-4|Fluoroscopic angiogram Guidance for atherectomy of Vein - right-- W contrast IV
30601-9|CT Guidance for biopsy of Abdomen
37913-1|US Guidance for biopsy of Abdomen
35890-3|Fluoroscopy Guidance for biopsy of Abdomen
44117-0|CT Guidance for biopsy of Abdomen retroperitoneum
44162-6|US Guidance for biopsy of Abdomen retroperitoneum
36767-2|CT Guidance for biopsy of Adrenal gland
35891-1|CT Guidance for biopsy of Bone
69076-8|Fluoroscopy Guidance for biopsy of Bone
37211-0|CT Guidance for biopsy of Bone marrow
35893-7|CT Guidance for biopsy of Breast
24602-5|Mammogram Guidance for biopsy of Breast
37914-9|US Guidance for biopsy of Breast
26337-6|Mammogram Guidance for biopsy of Breast - bilateral
69169-1|MRI Guidance for biopsy of Breast - bilateral
37912-3|US Guidance for biopsy of Breast - bilateral
26338-4|Mammogram Guidance for biopsy of Breast - left
69203-8|MRI Guidance for biopsy of Breast - left
42449-9|US Guidance for biopsy of Breast - left
26339-2|Mammogram Guidance for biopsy of Breast - right
69213-7|MRI Guidance for biopsy of Breast - right
42457-2|US Guidance for biopsy of Breast - right
35895-2|CT Guidance for biopsy of Chest
37915-6|US Guidance for biopsy of Chest
35894-5|Fluoroscopy Guidance for biopsy of Chest
37492-6|CT Guidance for biopsy of Chest.pleura
42333-5|US Guidance for biopsy of Chest.pleura
43567-7|CT Guidance for biopsy of Deep bone
43565-1|US Guidance for biopsy of Deep bone
44109-7|CT Guidance for biopsy of Deep muscle
42463-0|US Guidance for biopsy of Endomyocardium
37212-8|CT Guidance for biopsy of Epididymis
69387-9|US Guidance for biopsy of Epididymis
36927-2|CT Guidance for biopsy of Facial bones and Maxilla
35892-9|CT Guidance for biopsy of Head
42136-2|CT Guidance for biopsy of Heart
42279-0|CT Guidance for biopsy of Kidney
24772-6|US Guidance for biopsy of Kidney
35899-4|Fluoroscopy Guidance for biopsy of Kidney
38766-2|US Guidance for biopsy of Kidney transplant
30607-6|CT Guidance for biopsy of Kidney - bilateral
26340-0|US Guidance for biopsy of Kidney - bilateral
26341-8|US Guidance for biopsy of Kidney - left
26342-6|US Guidance for biopsy of Kidney - right
24812-0|CT Guidance for biopsy of Liver
24816-1|US Guidance for biopsy of Liver
35900-0|Fluoroscopy Guidance for biopsy of Liver
38765-4|US Guidance for biopsy of Liver transplant
35896-0|CT Guidance for biopsy of Lower extremity
24823-7|CT Guidance for biopsy of Lung
44161-8|US Guidance for biopsy of Lung
30634-0|Fluoroscopy Guidance for biopsy of Lung
35901-8|CT Guidance for biopsy of Lymph node
39522-8|US Guidance for biopsy of Lymph node
37213-6|CT Guidance for biopsy of Mediastinum
42137-0|US Guidance for biopsy of Mediastinum
36768-0|CT Guidance for biopsy of Muscle
37917-2|US Guidance for biopsy of Muscle
24838-5|CT Guidance for biopsy of Neck
37918-0|US Guidance for biopsy of Neck
30604-3|CT Guidance for biopsy of Pancreas
37919-8|US Guidance for biopsy of Pancreas
35902-6|Fluoroscopy Guidance for biopsy of Pancreas
24864-1|CT Guidance for biopsy of Pelvis
69074-3|Fluoroscopy Guidance for biopsy of Pelvis
35903-4|CT Guidance for biopsy of Prostate
24883-1|US Guidance for biopsy of Prostate
41802-0|Fluoroscopy Guidance for biopsy of Prostate
35898-6|CT Guidance for biopsy of Salivary gland
37920-6|US Guidance for biopsy of Salivary gland
69075-0|Fluoroscopy Guidance for biopsy of Salivary gland
38132-7|US Guidance for biopsy of Scrotum and Testicle
69396-0|US Guidance for biopsy of Spinal cord
35904-2|CT Guidance for biopsy of Spine Cervical
35905-9|CT Guidance for biopsy of Spine Lumbar
35906-7|CT Guidance for biopsy of Spine Thoracic
30609-2|CT Guidance for biopsy of Spleen
35907-5|Fluoroscopy Guidance for biopsy of Spleen
42265-9|CT Guidance for biopsy of Superficial bone
42135-4|US Guidance for biopsy of Superficial bone
38154-1|Fluoroscopy Guidance for biopsy of Superficial bone
43797-0|US Guidance for biopsy of Superficial lymph node
43564-4|US Guidance for biopsy of Superficial muscle
37214-4|CT Guidance for biopsy of Superficial tissue
35908-3|CT Guidance for biopsy of Thyroid
25009-2|US Guidance for biopsy of Thyroid
35897-8|CT Guidance for biopsy of Upper extremity
25044-9|CT Guidance for biopsy of Unspecified body region
25059-7|US Guidance for biopsy of Unspecified body region
25069-6|Fluoroscopy Guidance for biopsy of Unspecified body region
24670-2|US Guidance for biopsy of cyst of Unspecified body region
30651-4|US Guidance for core needle biopsy of Breast
24813-8|CT Guidance for core needle biopsy of Liver
69279-8|US Guidance for core needle biopsy of Lymph node
46285-3|US Guidance for core needle biopsy of Thyroid
38024-6|US Guidance for core needle biopsy of Unspecified body region
69073-5|Fluoroscopy Guidance for core needle biopsy of Unspecified body region
42448-1|US Guidance for excisional biopsy of Breast
30652-2|US Guidance for fine needle biopsy of Breast
42288-1|CT Guidance for needle biopsy of Abdomen
69224-4|Fluoroscopy Guidance for needle biopsy of Abdomen
46367-9|CT Guidance for needle biopsy of Adrenal gland
46368-7|CT Guidance for needle biopsy of Breast
46286-1|Mammogram Guidance for needle biopsy of Breast
38028-7|US Guidance for needle biopsy of Breast
41803-8|Fluoroscopy Guidance for needle biopsy of Breast
43462-1|US Guidance for needle biopsy of Breast - left
43447-2|Mammogram Guidance for needle biopsy of Breast - right
69290-5|US Guidance for needle biopsy of Breast - right
38029-5|US Guidance for needle biopsy of Chest
69225-1|Fluoroscopy Guidance for needle biopsy of Chest
69099-0|CT Guidance for needle biopsy of Chest.pleura
44171-7|US Guidance for needle biopsy of Chest.pleura
69127-9|Fluoroscopy Guidance for needle biopsy of Chest.pleura
43568-5|CT Guidance for needle biopsy of Deep bone
42289-9|CT Guidance for needle biopsy of Kidney
38027-9|US Guidance for needle biopsy of Kidney - bilateral
69097-4|CT Guidance for needle biopsy of Liver
69197-2|MRI Guidance for needle biopsy of Liver
44170-9|US Guidance for needle biopsy of Liver
69125-3|Fluoroscopy Guidance for needle biopsy of Liver
42267-5|CT Guidance for needle biopsy of Lymph node
37916-4|US Guidance for needle biopsy of Lymph node
69098-2|CT Guidance for needle biopsy of Muscle
69198-0|MRI Guidance for needle biopsy of Muscle
69288-9|US Guidance for needle biopsy of Muscle
69226-9|Fluoroscopy Guidance for needle biopsy of Muscle
46369-5|US Guidance for needle biopsy of Ovary
42290-7|CT Guidance for needle biopsy of Pancreas
69199-8|MRI Guidance for needle biopsy of Pancreas
69289-7|US Guidance for needle biopsy of Pancreas
69126-1|Fluoroscopy Guidance for needle biopsy of Pancreas
46370-3|US Guidance for needle biopsy of Pelvis
69200-4|MRI Guidance for needle biopsy of Pleura
69227-7|Fluoroscopy Guidance for needle biopsy of Pleura
46288-7|US Guidance for needle biopsy of Prostate
69228-5|Fluoroscopy Guidance for needle biopsy of Prostate
69100-6|CT Guidance for needle biopsy of Salivary gland
69201-2|MRI Guidance for needle biopsy of Salivary gland
69291-3|US Guidance for needle biopsy of Salivary gland
69128-7|Fluoroscopy Guidance for needle biopsy of Salivary gland
43571-9|CT Guidance for needle biopsy of Soft bone
69401-8|US Guidance for needle biopsy of Spinal cord
38030-3|US Guidance for needle biopsy of Spleen
42266-7|CT Guidance for needle biopsy of Superficial bone
69101-4|CT Guidance for needle biopsy of Thyroid
69202-0|MRI Guidance for needle biopsy of Thyroid
38031-1|US Guidance for needle biopsy of Thyroid
69129-5|Fluoroscopy Guidance for needle biopsy of Thyroid
46287-9|CT Guidance for needle biopsy of Unspecified body region
30700-9|US Guidance for needle biopsy of Unspecified body region
44225-1|Fluoroscopy Guidance for needle biopsy of Liver-- W contrast IV
24718-9|Fluoroscopy Guidance for transjugular biopsy of Liver-- W contrast IV
35910-9|CT Guidance for biopsy of Chest-- W and WO contrast IV
46289-5|CT Guidance for biopsy of Unspecified body region-- W and WO contrast IV
35909-1|CT Guidance for biopsy of Chest-- W contrast IV
69093-3|CT Guidance for biopsy of Pelvis-- W contrast IV
42260-0|CT Guidance for biopsy of Unspecified body region-- W contrast IV
46366-1|SPECT Guidance for biopsy of Bone
46384-4|SPECT Guidance for biopsy of Superficial bone
69083-4|CT Guidance for biopsy of Abdomen-- WO contrast
35911-7|CT Guidance for biopsy of Chest-- WO contrast
69092-5|CT Guidance for biopsy of Liver-- WO contrast
69094-1|CT Guidance for biopsy of Pelvis-- WO contrast
46290-3|CT Guidance for biopsy of Unspecified body region-- WO contrast
35889-5|Fluoroscopy Guidance for bronchoscopy of Chest
64998-8|Fluoroscopy Guidance for catheterization of Fallopian tube - left-- transcervical
64999-6|Fluoroscopy Guidance for catheterization of Fallopian tube -right-- transcervical
30818-9|Fluoroscopy Guidance for catheterization of Fallopian tubes-- transcervical
30892-4|Fluoroscopy Guidance for catheterization of Biliary ducts and Pancreatic duct-- W contrast retrograde
24624-9|Fluoroscopic angiogram Guidance for change of central catheter in Central vein-- W contrast IV
26331-9|Fluoroscopic angiogram Guidance for change of central catheter in Central vein - bilateral-- W contrast IV
26332-7|Fluoroscopic angiogram Guidance for change of central catheter in Central vein - left-- W contrast IV
26333-5|Fluoroscopic angiogram Guidance for change of central catheter in Central vein - right-- W contrast IV
43558-6|Fluoroscopy Guidance for change of dialysis catheter in Unspecified body region-- W contrast IV
36769-8|CT Guidance for change of nephrostomy tube in Kidney
24781-7|Fluoroscopy Guidance for change of percutaneous nephrostomy tube in Kidney - bilateral-- W contrast
46371-1|X-ray Guidance for change of percutaneous tube in Unspecified body region-- W contrast
30646-4|Fluoroscopy Guidance for change of tube in Sinus tract-- W contrast
69400-0|US Guidance for chorionic villus sampling
69391-1|US Guidance for cordocentesis
70915-4|US Guidance for CSF aspiration of Spine Cervical
70916-2|US Guidance for CSF aspiration of Spine Lumbar
70917-0|US Guidance for CSF aspiration of Spine Thoracic
24680-1|Fluoroscopy Guidance for dilation of Esophagus
35913-3|CT Guidance for drainage of Abdomen
42287-3|CT Guidance for drainage of Abdomen retroperitoneum
41809-5|US Guidance for drainage of Abdomen retroperitoneum
35914-1|CT Guidance for drainage of Anus
35915-8|CT Guidance for drainage of Appendix
36770-6|CT Guidance for drainage of Biliary ducts and Gallbladder
35916-6|CT Guidance for drainage of Chest
69078-4|Fluoroscopy Guidance for drainage of Chest
24692-6|US Guidance for drainage of Extremity
26325-1|US Guidance for drainage of Extremity - bilateral
26326-9|US Guidance for drainage of Extremity - left
26327-7|US Guidance for drainage of Extremity - right
35917-4|CT Guidance for drainage of Gallbladder
69133-7|Fluoroscopy Guidance for drainage of Hip
35918-2|CT Guidance for drainage of Kidney
24896-3|US Guidance for drainage of Kidney
26328-5|US Guidance for drainage of Kidney - bilateral
26329-3|US Guidance for drainage of Kidney - left
26330-1|US Guidance for drainage of Kidney - right
35919-0|CT Guidance for drainage of Liver
35920-8|CT Guidance for drainage of Lymph node
42283-2|CT Guidance for drainage of Pancreas
44172-5|US Guidance for drainage of Pancreas
35921-6|CT Guidance for drainage of Pelvis
24868-2|US Guidance for drainage of Pelvis
41800-4|Fluoroscopy Guidance for drainage of Pharynx
41798-0|US Guidance for drainage of Prostate
35922-4|CT Guidance for drainage of Unspecified body region
30699-3|US Guidance for drainage of Unspecified body region
43537-0|Fluoroscopy Guidance for drainage of Unspecified body region
42478-8|US Guidance for drainage of cyst of Kidney
46291-1|CT Guidance for drainage of Unspecified body region-- W and WO contrast IV
35923-2|CT Guidance for drainage of Chest-- W contrast IV
46292-9|CT Guidance for drainage of Unspecified body region-- W contrast IV
35924-0|CT Guidance for drainage of Chest-- WO contrast
46293-7|CT Guidance for drainage of Unspecified body region-- WO contrast
35925-7|Fluoroscopy Guidance for endoscopy of Stomach
43478-7|Fluoroscopy Guidance for endoscopy of Biliary ducts and Pancreatic duct-- 1.5 hours post contrast retrograde
43474-6|Fluoroscopy Guidance for endoscopy of Biliary ducts and Pancreatic duct-- 15 minutes post contrast retrograde
43477-9|Fluoroscopy Guidance for endoscopy of Biliary ducts and Pancreatic duct-- 1 hour post contrast retrograde
43473-8|Fluoroscopy Guidance for endoscopy of Biliary ducts and Pancreatic duct-- 2 hours post contrast retrograde
43475-3|Fluoroscopy Guidance for endoscopy of Biliary ducts and Pancreatic duct-- 30 minutes post contrast retrograde
43476-1|Fluoroscopy Guidance for endoscopy of Biliary ducts and Pancreatic duct-- 45 minutes post contrast retrograde
72248-8|Abdomen MRCP with and without contrast IV
44214-5|Fluoroscopy Guidance for endoscopy of Biliary ducts-- W contrast retrograde
30815-5|Fluoroscopy Guidance for endoscopy of Biliary ducts and Pancreatic duct-- W contrast retrograde
44213-7|Fluoroscopy Guidance for endoscopy of Pancreatic duct-- W contrast retrograde
58740-2|Abdomen MRCP WO contrast
72541-6|Fluoroscopy Guidance for facet joint denervation of Spine Cervical
72542-4|Fluoroscopy Guidance for facet joint denervation of Spine Lumbar
72540-8|Fluoroscopy Guidance for facet joint denervation of Spine
35926-5|Fluoroscopy Guidance for gastrostomy of Stomach
30638-1|Fluoroscopy Guidance for injection of Hip
24769-2|CT Guidance for injection of Joint space
42334-3|Fluoroscopy Guidance for injection of Mammary artery.internal - left
42706-2|US Guidance for injection of Pleural space
24901-1|CT Guidance for injection of Sacroiliac Joint
35927-3|Fluoroscopy Guidance for injection of Sacroiliac Joint
26319-4|CT Guidance for injection of Sacroiliac joint - bilateral
26320-2|CT Guidance for injection of Sacroiliac joint - left
26321-0|CT Guidance for injection of Sacroiliac joint - right
48435-2|Fluoroscopy Guidance for injection of Salivary gland - bilateral
46392-7|Fluoroscopy Guidance for injection of Sinuses
30579-7|CT Guidance for injection of Spine facet joint
24931-8|Fluoroscopy Guidance for injection of Spine facet joint
26322-8|Fluoroscopy Guidance for injection of Spine facet joint - bilateral
26323-6|Fluoroscopy Guidance for injection of Spine facet joint - left
26324-4|Fluoroscopy Guidance for injection of Spine facet joint - right
70918-8|Fluoroscopy Guidance for injection of Spine Cervical
30812-2|Fluoroscopy Guidance for injection of Spine Cervical Facet Joint
37493-4|CT Guidance for injection of Spine.disc.cervical
70919-6|Fluoroscopy Guidance for injection of Spine Lumbar
30817-1|Fluoroscopy Guidance for injection of Spine Lumbar Facet Joint
70920-4|Fluoroscopy Guidance for injection of Spine Thoracic
30814-8|Fluoroscopy Guidance for injection of Spine Thoracic Facet Joint
30702-5|US Guidance for injection of Thyroid
72530-9|US Guidance for injection of Joint
36771-4|Fluoroscopy Guidance for injection of Joint
37494-2|Fluoroscopy Guidance for injection of Tendon
72537-4|US Guidance for injection of sclerosing agent of Extremity vein - bilateral
72645-5|US Guidance for injection of sclerosing agent of Extremity vein - left
72644-8|US Guidance for injection of sclerosing agent of Extremity vein - right
72536-6|US Guidance for injection of sclerosing agent of Extremity veins - bilateral
72643-0|US Guidance for injection of sclerosing agent of Extremity veins - left
72642-2|US Guidance for injection of sclerosing agent of Extremity veins - right
72543-2|Fluoroscopy Guidance for intercostal nerve devervation of Spine Thoracic
72552-3|Fluoroscopy Guidance for kyphoplasty of Spine Lumbar
72553-1|Fluoroscopy Guidance for kyphoplasty of Spine Thoracic
72535-8|US Guidance for laser ablation of vein(s) of Extremity vein - left
72534-1|US Guidance for laser ablation of vein(s) of Extremity vein - right
48735-5|Mammogram Guidance for localization of Breast
43759-0|US Guidance for localization of Breast - bilateral
35928-1|CT Guidance for localization of Breast - left
42296-4|Mammogram Guidance for localization of Breast - left
43758-2|US Guidance for localization of Breast - left
35929-9|CT Guidance for localization of Breast - right
42297-2|Mammogram Guidance for localization of Breast - right
43760-8|US Guidance for localization of Breast - right
37608-7|US Guidance for localization of foreign body of Eye
42701-3|CT Guidance for localization of placenta of Uterus
39760-4|Scan Guidance for localization of tumor limited
39759-6|SPECT Guidance for localization of tumor limited
39761-2|Scan Guidance for localization of tumor limited-- W Tc-99m Sestamibi IV
39953-5|Scan Guidance for localization of tumor multiple areas
39763-8|Scan Guidance for localization of tumor
39762-0|SPECT Guidance for localization of tumor
39758-8|Scan Guidance for localization of tumor of Breast
44110-5|CT Guidance for needle localization of Breast
24600-9|US Guidance for needle localization of Breast
69068-5|Mammogram Guidance for needle localization of Breast - bilateral
26313-7|US Guidance for needle localization of Breast - bilateral
26314-5|US Guidance for needle localization of Breast - left
26318-6|US Guidance for needle localization of Breast - right
37921-4|US Guidance for needle localization of Chest
42021-6|CT Guidance for needle localization of Spine Cervical
42020-8|CT Guidance for needle localization of Spine Lumbar
39026-0|CT Guidance for needle localization of Unspecified body region
39028-6|MRI Guidance for needle localization of Unspecified body region
38032-9|US Guidance for needle localization of Unspecified body region
39027-8|Fluoroscopy Guidance for needle localization of Unspecified body region
24595-1|Mammogram Guidance for needle localization of mass of Breast
26315-2|Mammogram Guidance for needle localization of mass of Breast - bilateral
26316-0|Mammogram Guidance for needle localization of mass of Breast - left
26317-8|Mammogram Guidance for needle localization of mass of Breast - right
44118-8|CT Guidance for needle localization of Breast-- W and WO contrast IV
35930-7|CT Guidance for nerve block of Abdomen
35931-5|CT Guidance for nerve block of Pelvis
70921-2|CT Guidance for nerve block of Spine Cervical
35932-3|CT Guidance for nerve block of Spine Lumbar
70922-0|CT Guidance for nerve block of Spine Thoracic
69240-0|Fluoroscopy Guidance for percutaneous biopsy of Abdomen
42139-6|US Guidance for percutaneous biopsy of Muscle
24609-0|Mammogram Guidance for core needle percutaneous biopsy of Breast
26334-3|Mammogram Guidance for core needle percutaneous biopsy of Breast - bilateral
26335-0|Mammogram Guidance for core needle percutaneous biopsy of Breast - left
38023-8|US Guidance for core needle percutaneous biopsy of Breast - left
26336-8|Mammogram Guidance for core needle percutaneous biopsy of Breast - right
38025-3|US Guidance for core needle percutaneous biopsy of Breast - right
44121-2|Mammogram Guidance for percutaneous needle biopsy of Breast
69245-9|Fluoroscopy Guidance for percutaneous needle biopsy of Kidney
69246-7|Fluoroscopy Guidance for percutaneous needle biopsy of Liver
44204-6|Fluoroscopy Guidance for percutaneous needle biopsy of Lung
69247-5|Fluoroscopy Guidance for percutaneous needle biopsy of Salivary gland
46372-9|Fluoroscopy Guidance for percutaneous drainage of Biliary ducts
62494-0|US Guidance for percutaneous drainage of Cavity
24621-5|Fluoroscopy Guidance for percutaneous drainage of Cavity
69241-8|Fluoroscopy Guidance for percutaneous drainage of abscess of Abdomen
69242-6|Fluoroscopy Guidance for percutaneous drainage of abscess of Appendix
42422-6|Fluoroscopy Guidance for percutaneous drainage of abscess of Breast
43444-9|CT Guidance for percutaneous drainage of abscess of Cavity
42423-4|Fluoroscopy Guidance for percutaneous drainage of abscess of Chest
69243-4|Fluoroscopy Guidance for percutaneous drainage of abscess of Lung
44223-6|Fluoroscopy Guidance for percutaneous drainage of abscess of Ovary
69244-2|Fluoroscopy Guidance for percutaneous drainage of abscess of Pelvis
42421-8|Fluoroscopy Guidance for percutaneous drainage of abscess of Unspecified body region
70923-8|Fluoroscopy Guidance for percutaneous vertebroplasty of Spine Cervical
35934-9|CT Guidance for percutaneous vertebroplasty of Spine Lumbar
70924-6|Fluoroscopy Guidance for percutaneous vertebroplasty of Spine Lumbar
35935-6|CT Guidance for percutaneous vertebroplasty of Spine Thoracic
70925-3|Fluoroscopy Guidance for percutaneous vertebroplasty of Spine Thoracic
72539-0|Fluoroscopy Guidance for peripheral nerve denervation of Unspecified body region
30643-1|US Guidance for placement of catheter in Central vein
35912-5|Fluoroscopy Guidance for placement of catheter in Unspecified body region
25028-2|Fluoroscopic angiogram Guidance for placement of catheter for adminstration of thrombolytic in Vessel
25029-0|Fluoroscopic angiogram Guidance for placement of catheter for vasoconstrictor infusion in Vessels
24613-2|Fluoroscopic angiogram Guidance for placement of catheter in artery in Central cardiovascular artery
30644-9|US Guidance for placement of catheter in Central vein-- Tunneled
25077-9|Fluoroscopic angiogram Guidance for placement of catheter in Hepatic artery-- W contrast IA
24625-6|Fluoroscopic angiogram Guidance for placement of catheter in Central vein-- W contrast IV
26310-3|Fluoroscopic angiogram Guidance for placement of catheter in Central vein - bilateral-- W contrast IV
26311-1|Fluoroscopic angiogram Guidance for placement of catheter in Central vein - left-- W contrast IV
26312-9|Fluoroscopic angiogram Guidance for placement of catheter in Central vein - right-- W contrast IV
41801-2|Fluoroscopic angiogram Guidance for placement of catheter in Portal vein-- W contrast IV
24716-3|Fluoroscopy Guidance for placement of decompression tube in Gastrointestine
62491-6|Fluoroscopic angiogram Guidance for placement of ilio-iliac tube endoprosthesis in Iliac artery - left-- W contrast IA
62492-4|Fluoroscopic angiogram Guidance for placement of ilio-iliac tube endoprosthesis in Iliac artery - right-- W contrast IA
25072-0|Guidance for placement of infusion port in Unspecified body region
62450-2|Fluoroscopic angiogram Guidance for placement of intraperitoneal catheter in Abdomen
25026-6|Fluoroscopic angiogram Guidance for placement of IVC filter in Inferior vena cava-- W contrast IV
25027-4|Guidance for placement of large bore catheter into vessel in Central vein
26307-9|Guidance for placement of large bore catheter into vessel in Central vein - bilateral
26308-7|Guidance for placement of large bore catheter into vessel in Central vein - left
26309-5|Guidance for placement of large bore catheter into vessel in Central vein - right
25024-1|Fluoroscopic angiogram Guidance for placement of longterm peripheral catheter in Central vein
26304-6|Fluoroscopic angiogram Guidance for placement of longterm peripheral catheter in Central vein - bilateral
26305-3|Fluoroscopic angiogram Guidance for placement of longterm peripheral catheter in Central vein - left
26306-1|Fluoroscopic angiogram Guidance for placement of longterm peripheral catheter in Central vein - right
64993-9|US Guidance for placement of needle in Unspecified body region
42456-4|US Guidance for placement of needle wire in Breast
36772-2|CT Guidance for placement of nephrostomy tube in Kidney
24779-1|Fluoroscopy Guidance for placement of percutaneous nephrostomy in Kidney - bilateral-- W contrast via tube
24782-5|Fluoroscopy Guidance for placement of percutaneous nephroureteral stent in Kidney - bilateral
35937-2|CT Guidance for placement of radiation therapy fields in Unspecified body region
43487-8|US Guidance for placement of radiation therapy fields in Unspecified body region
65797-3|Fluoroscopic angiogram Guidance for placement of stent in Artery - left
65798-1|Fluoroscopic angiogram Guidance for placement of stent in Artery - right
69134-5|Fluoroscopic angiogram Guidance for placement of stent in Iliac artery
25078-7|Fluoroscopy Guidance for placement of stent in Intrahepatic portal system
24756-9|Fluoroscopic angiogram Guidance for placement of stent in Vein
26301-2|Fluoroscopic angiogram Guidance for placement of stent in Vein - bilateral
26302-0|Fluoroscopic angiogram Guidance for placement of stent in Vein - left
26303-8|Fluoroscopic angiogram Guidance for placement of stent in Vein - right
24555-5|Fluoroscopic angiogram Guidance for placement of stent in Artery
51391-1|Fluoroscopic angiogram Guidance for placement of transjugular intrahepatic portosystemic shunt in Portal vein and Hepatic vein
35938-0|CT Guidance for placement of tube in Chest
42140-4|US Guidance for placement of tube in Chest
39362-9|Fluoroscopy Guidance for placement of tube in Chest
30637-3|Fluoroscopy Guidance for placement of tube in Gastrointestine
41799-8|Fluoroscopy Guidance for placement of tube in Liver
24995-3|Fluoroscopy Guidance for placement of tube in Stomach
44224-4|Fluoroscopy Guidance for placement of tube in Unspecified body region
46373-7|SPECT Guidance for placement of tube in Chest
44102-2|CT Guidance for procedure of Joint space
44222-8|Fluoroscopy Guidance for procedure of Joint space
30629-0|Fluoroscopy Guidance for procedure of Unspecified body region
30581-3|CT Guidance for radiation treatment of Unspecified body region-- W contrast IV
30664-7|MRI Guidance for radiation treatment of Unspecified body region-- W contrast IV
30582-1|CT Guidance for radiation treatment of Unspecified body region-- WO contrast
30665-4|MRI Guidance for radiation treatment of Unspecified body region-- WO contrast
25053-0|CT Guidance for radiosurgery of Unspecified body region
25054-8|CT Guidance for radiosurgery of Unspecified body region-- W contrast IV
24537-3|US Guidance for removal of amniotic fluid from Uterus
42141-2|US Guidance for removal of catheter from Central vein-- Tunneled
72549-9|Fluoroscopy Guidance for removal of catheter from Central vein-- Tunneled
72548-1|Fluoroscopic angiogram Guidance for removal of catheter from Central vein-- W contrast IV
72547-3|Fluoroscopy Guidance for removal of CVA device obstruction from Central vein
72546-5|Fluoroscopy Guidance for removal of CVA lumen obstruction from Central vein
41810-3|CT Guidance for removal of fluid from Abdomen
24559-7|US Guidance for removal of fluid from Abdomen
38142-6|US Guidance for removal of fluid from Chest
30628-2|Fluoroscopy Guidance for removal of foreign body from Unspecified body region
72538-2|Fluoroscopic angiogram Guidance for removal of longterm peripheral catheter from Central vein
72544-0|Fluoroscopy Guidance for removal of percutaneous nephrostomy tube from Kidney - bilateral-- W contrast
24885-6|US Guidance for repair of Pseudoaneurysm/AV fistula
72550-7|Fluoroscopy Guidance for repair of CVA catheter with port or pump of Central vein
72551-5|Fluoroscopy Guidance for repair of CVA catheter without port or pump of Central vein
42017-4|Fluoroscopy Guidance for replacement of percutaneous cholecystostomy in Abdomen
52790-3|CT Guidance for replacement of percutaneous drainage tube in Abdomen
72545-7|Fluoroscopy Guidance for replacement of percutaneous drainage tube in Biliary ducts and Gallbladder
52791-1|CT Guidance for replacement of percutaneous drainage tube in Pelvis
46294-5|Fluoroscopy Guidance for replacement of percutaneous drainage tube in Stomach
24996-1|Fluoroscopy Guidance for replacement of percutaneous gastrostomy in Stomach
24626-4|Fluoroscopic angiogram Guidance for reposition of catheter in Central vein-- W contrast IV
26295-6|Fluoroscopic angiogram Guidance for reposition of catheter in Central vein - bilateral-- W contrast IV
26296-4|Fluoroscopic angiogram Guidance for reposition of catheter in Central vein - left-- W contrast IV
26297-2|Fluoroscopic angiogram Guidance for reposition of catheter in Central vein - right-- W contrast IV
48740-5|Mammogram Guidance for sentinel lymph node injection of Breast
48736-3|Mammogram Guidance for sentinel lymph node injection of Breast - left
48739-7|Mammogram Guidance for sentinel lymph node injection of Breast - right
24570-4|Fluoroscopy Guidance for stone removal of Biliary duct common-- W contrast intra biliary duct
43763-2|Fluoroscopic angiogram Guidance for thrombectomy of Vein-- W contrast IV
43761-6|Fluoroscopic angiogram Guidance for thrombectomy of Vein - bilateral-- W contrast IV
43762-4|Fluoroscopic angiogram Guidance for thrombectomy of Vein - left-- W contrast IV
43764-0|Fluoroscopic angiogram Guidance for thrombectomy of Vein - right-- W contrast IV
72554-9|Fluoroscopy Guidance for trigger point injection of Muscle
39138-3|Fluoroscopic angiogram Guidance for vascular access of Vessel
39139-1|US Guidance for vascular access of Unspecified body region
36936-3|MRI Guidance.stereotactic for biopsy of Brain
24603-3|Mammogram Guidance.stereotactic for biopsy of Breast
26292-3|Mammogram Guidance.stereotactic for biopsy of Breast - bilateral
26293-1|Mammogram Guidance.stereotactic for biopsy of Breast - left
26294-9|Mammogram Guidance.stereotactic for biopsy of Breast - right
36928-0|CT Guidance.stereotactic for biopsy of Head
46296-0|Mammogram Guidance.stereotactic for core needle biopsy of Breast
46295-2|Mammogram Guidance.stereotactic for core needle biopsy of Breast - left
42433-3|Mammogram Guidance.stereotactic for core needle biopsy of Breast - right
69160-0|Mammogram Guidance.stereotactic for needle biopsy of Breast
24585-2|CT Guidance.stereotactic for biopsy of Head-- W contrast IV
36929-8|CT Guidance.stereotactic for biopsy of Head-- WO contrast
44122-0|MRI Guidance.stereotactic for localization in Brain-- W and WO contrast IV
30656-3|MRI Guidance.stereotactic for localization in Brain-- W contrast IV
30800-7|MRI Guidance.stereotactic for localization in Brain-- WO contrast
24655-3|Chest Fluoroscopy Image intensifier during surgery
24717-1|Ileal conduit X-ray Loopogram
24672-8|Diaphragm US Motion
30632-4|Diaphragm Fluoroscopy Motion
35990-1|Fetal MRI
41806-1|Abdomen CT
24556-3|Abdomen MRI
24558-9|Abdomen US
30762-9|Abdomen X-ray tomograph
24566-2|Abdomen retroperitoneum CT
24531-6|Abdomen retroperitoneum US
24532-4|Abdomen RUQ US
44115-4|Abdomen and Pelvis CT
36781-3|Abdominal veins MRI angiogram
30864-3|Abdominal veins and IVC MRI angiogram
36791-2|Abdominal vessels MRI angiogram
24534-0|Abdominal vessels US.doppler
39494-0|Abdominal wall US
36930-6|Adrenal gland CT
36931-4|Adrenal gland MRI
69277-2|Adrenal gland US
36792-0|Adrenal vessels MRI angiogram
35940-6|Ankle CT
24538-1|Ankle MRI
35939-8|Ankle X-ray tomograph
35941-4|Ankle - bilateral CT
26208-9|Ankle - bilateral MRI
35942-2|Ankle - left CT
26209-7|Ankle - left MRI
35943-0|Ankle - left X-ray tomograph
35944-8|Ankle - right CT
26210-5|Ankle - right MRI
37674-9|Ankle - right X-ray tomograph
37222-7|Ankle and Foot MRI
24542-3|Anus US
35945-5|Aorta CT
35947-1|Aorta MRI
35946-3|Aorta MRI angiogram
24547-2|Aorta US
46388-5|Aorta US.doppler
35948-9|Aorta abdominal CT
35949-7|Aorta abdominal MRI
69276-4|Aorta abdominal US
37216-9|Aorta.endograft CT
24544-9|Aorta thoracic CT
35950-5|Aorta thoracic MRI
24660-3|Aorta thoracic MRI angiogram
30863-5|Abdominal Aorta and Arteries MRI angiogram
35951-3|Aortic arch MRI angiogram
30861-9|Aortic arch and Neck vessels MRI angiogram
35952-1|Appendix CT
24548-0|Appendix US
39040-1|AV fistula US
43508-1|Axilla - left MRI
72529-1|Axilla - left US
43510-7|Axilla - right MRI
72528-3|Axilla - right US
37219-3|Biliary ducts MRI
38021-2|Biliary ducts and Gallbladder US
37220-1|Biliary ducts and Pancreatic duct MRI
39039-3|Brachiocephalic artery US.doppler
24590-2|Brain MRI
58748-5|Brain Functional MRI
44138-6|Brain PET
37217-7|Brain Stem and Nerves.cranial MRI
37218-5|Brain.temporal MRI
43772-3|Brain and Internal auditory canal MRI
42385-5|Brain and Pituitary and Sella turcica MRI
30794-2|Breast MRI
24601-7|Breast US
69165-9|Breast implant - bilateral MRI
38057-6|Breast implant - left MRI
38058-4|Breast implant - right MRI
24596-9|Breast specimen US
69397-8|Breast vessels US.doppler
30795-9|Breast - bilateral MRI
26214-7|Breast - bilateral US
35954-7|Breast - left MRI
26215-4|Breast - left US
35955-4|Breast - right MRI
26216-2|Breast - right US
46299-4|Breast - unilateral MRI
36010-7|Calcaneus CT
36011-5|Calcaneus X-ray tomograph
24616-5|Carotid artery US
42146-1|Carotid artery US.doppler
26217-0|Carotid artery - bilateral US
43765-7|Carotid artery - bilateral US.doppler
26218-8|Carotid artery - left US
39427-0|Carotid artery - left US.doppler
26219-6|Carotid artery - right US
39437-9|Carotid artery - right US.doppler
43552-9|Carotid artery - unilateral US
36793-8|Carotid vessel MRI angiogram
30859-3|Carotid vessels and Neck Vessels MRI angiogram
30865-0|Celiac vessels and Superior mesenteric Vessels MRI angiogram
46374-5|Cerebral artery US
24627-2|Chest CT
24629-8|Chest MRI
24630-6|Chest US
24657-9|Chest X-ray tomograph
30862-7|Chest vessels MRI angiogram
38016-2|Chest wall US
37235-9|Circle of Willis MRI angiogram
35960-4|Clavicle CT
35961-2|Clavicle MRI
35959-6|Clavicle X-ray tomograph
44120-4|Colon CT
24757-7|Coronary arteries CT fast
35962-0|Elbow CT
24674-4|Elbow MRI
35963-8|Elbow X-ray tomograph
35965-3|Elbow - bilateral CT
26220-4|Elbow - bilateral MRI
35964-6|Elbow - bilateral X-ray tomograph
35966-1|Elbow - left CT
26221-2|Elbow - left MRI
35967-9|Elbow - left X-ray tomograph
35968-7|Elbow - right CT
26222-0|Elbow - right MRI
37688-9|Elbow - right X-ray tomograph
35969-5|Esophagus CT
57823-7|Esophagus PET
24690-0|Extremity CT
69193-1|Extremity MRI
24693-4|Extremity US
35970-3|Extremity X-ray tomograph
39042-7|Extremity artery US.doppler
39031-0|Extremity artery - bilateral US.doppler
69293-9|Extremity artery - left US
39428-8|Extremity artery - left US.doppler
69297-0|Extremity artery - right US
39439-5|Extremity artery - right US.doppler
39449-4|Extremity vein US.doppler
39418-9|Extremity vein - bilateral US.doppler
42145-3|Extremity vein - left US
39429-6|Extremity vein - left US.doppler
42144-6|Extremity vein - right US
39440-3|Extremity vein - right US.doppler
30876-7|Extremity veins MRI angiogram
69283-0|Extremity veins - bilateral US.doppler
41835-0|Extremity veins - left US
41816-0|Extremity veins - right US
36794-6|Extremity vessels MRI angiogram
43771-5|Extremity vessels US.doppler
39495-7|Extremity vessels - bilateral US.doppler
69398-6|Extremity vessels Left US.doppler
39503-8|Extremity vessels - right US.doppler
26224-6|Extremity - bilateral CT
26223-8|Extremity - bilateral US
26226-1|Extremity - left CT
26225-3|Extremity - left US
26231-1|Extremity - right CT
26230-3|Extremity - right US
35953-9|Face MRI
41808-7|Facial bones and Maxilla CT
24696-7|Facial bones and Sinuses CT
69389-5|Femoral artery and Popliteal artery US
69399-4|Femoral vein and Popliteal vein US
30871-8|Femoral vessels MRI angiogram
38134-3|Femoral vessels US
38128-5|Femoral vessels - bilateral US
39498-1|Femoral vessels - left US.doppler
39504-6|Femoral vessels - right US.doppler
35984-4|Femur CT
35985-1|Femur X-ray tomograph
35986-9|Femur - bilateral X-ray tomograph
35987-7|Femur - left CT
38037-8|Femur - left US
35988-5|Femur - left X-ray tomograph
35989-3|Femur - right CT
38048-5|Femur - right US
38768-8|Femur - right X-ray tomograph
24705-6|Finger MRI
26238-6|Finger - bilateral MRI
26239-4|Finger - left MRI
26240-2|Finger - right MRI
37221-9|Fistula CT
35991-9|Foot CT
24707-2|Foot MRI
35992-7|Foot X-ray tomograph
30872-6|Foot vessels MRI angiogram
46362-0|Foot vessels US.doppler
35993-5|Foot - bilateral CT
26241-0|Foot - bilateral MRI
35994-3|Foot - left CT
26242-8|Foot - left MRI
35995-0|Foot - left X-ray tomograph
35996-8|Foot - right CT
26243-6|Foot - right MRI
37706-9|Foot - right X-ray tomograph
35997-6|Forearm CT
24710-6|Forearm MRI
30873-4|Forearm vessels MRI angiogram
35998-4|Forearm - bilateral CT
26244-4|Forearm - bilateral MRI
35999-2|Forearm - left CT
26245-1|Forearm - left MRI
36000-8|Forearm - right CT
26246-9|Forearm - right MRI
24711-4|Gallbladder US
36001-6|Gallbladder X-ray tomograph
39415-5|Gastrointestine US
39416-3|Genitourinary system US
37236-7|Great vessel MRI
24719-7|Groin US
36002-4|Hand CT
24720-5|Hand MRI
36003-2|Hand X-ray tomograph
46382-8|Hand vessels US.doppler
36004-0|Hand - bilateral CT
26247-7|Hand - bilateral MRI
36005-7|Hand - left CT
26248-5|Hand - left MRI
36006-5|Hand - left X-ray tomograph
36007-3|Hand - right CT
26249-3|Hand - right MRI
37717-6|Hand - right X-ray tomograph
24725-4|Head CT
24728-8|Head CT cine
24731-2|Head US
58741-0|Head to thigh PET
30858-5|Head veins MRI angiogram
30856-9|Head vessels MRI angiogram
24733-8|Head vessels US.doppler
42304-6|Head vessels and Neck vessels MRI angiogram
30880-9|Head vessels and Neck vessels US.doppler
30655-5|Head Cistern MRI
24746-0|Head Sagittal Sinus MRI
58742-8|Head and Neck PET
44164-2|Head and Neck US
58744-4|Heart CT
24748-6|Heart MRI
36009-9|Heart MRI angiogram
44137-8|Heart PET
42148-7|Heart US
36014-9|Hip CT
36013-1|Hip MRI
24760-1|Hip US
36012-3|Hip X-ray tomograph
36016-4|Hip - bilateral CT
36017-2|Hip - bilateral MRI
26250-1|Hip - bilateral US
36015-6|Hip - bilateral X-ray tomograph
36018-0|Hip - left CT
36020-6|Hip - left MRI
26251-9|Hip - left US
36019-8|Hip - left X-ray tomograph
36021-4|Hip - right CT
36022-2|Hip - right MRI
26252-7|Hip - right US
37735-8|Hip - right X-ray tomograph
43566-9|Hip and Thigh US
36024-8|Humerus X-ray tomograph
39425-4|Iliac artery US.doppler
42147-9|Iliac graft US.doppler
39497-3|Iliac vessels US.doppler
38129-3|Iliac vessels - bilateral US
38137-6|Iliac vessels - left US
38141-8|Iliac vessels - right US
35958-8|Internal auditory canal CT
35956-2|Internal auditory canal MRI
24767-6|Internal auditory canal X-ray tomograph
26253-5|Internal auditory canal - bilateral X-ray tomograph
35957-0|Internal auditory canal - left CT
26254-3|Internal auditory canal - left X-ray tomograph
38767-0|Internal auditory canal - right CT
26255-0|Internal auditory canal - right X-ray tomograph
24735-3|Internal auditory canal and Posterior fossa MRI
36033-9|Kidney MRI
38036-0|Kidney US
36032-1|Kidney X-ray tomograph
39032-8|Kidney transplant US
42477-0|Kidney vessels transplant US.doppler
43767-3|Kidney - bilateral CT
36034-7|Kidney - bilateral MRI
43774-9|Kidney - bilateral US
24789-0|Kidney - bilateral X-ray tomograph
69402-6|Kidney Bilateral and Bladder US
36035-4|Kidney - left MRI
38038-6|Kidney - left US
69113-9|Kidney - right CT
36036-2|Kidney - right MRI
38049-3|Kidney - right US
36037-0|Knee CT
24802-1|Knee MRI
36038-8|Knee X-ray tomograph
36799-5|Knee vessels MRI angiogram
36800-1|Knee vessels - left MRI angiogram
36801-9|Knee vessels - right MRI angiogram
36040-4|Knee - bilateral CT
26256-8|Knee - bilateral MRI
36039-6|Knee - bilateral X-ray tomograph
36041-2|Knee - left CT
26257-6|Knee - left MRI
36042-0|Knee - left X-ray tomograph
36043-8|Knee - right CT
26258-4|Knee - right MRI
37760-6|Knee - right X-ray tomograph
36045-3|Larynx MRI
36044-6|Larynx X-ray tomograph
24814-6|Liver CT
36046-1|Liver MRI
28614-6|Liver US
39454-4|Liver transplant US
24818-7|Liver and Diaphragm US
35971-1|Lower extremity CT
30692-8|Lower extremity MRI
30709-0|Lower extremity US
35972-9|Lower extremity X-ray tomograph
48693-6|Lower extremity artery US
39434-6|Lower extremity artery US.doppler
38130-1|Lower extremity artery - bilateral US
39421-3|Lower extremity artery - bilateral US.doppler
41834-3|Lower extremity artery - left US
39499-9|Lower extremity artery - left US.doppler
41815-2|Lower extremity artery - right US
39505-3|Lower extremity artery - right US.doppler
46363-8|Lower extremity vein US
30881-7|Lower extremity vein US.doppler
46364-6|Lower extremity vein - bilateral US
39420-5|Lower extremity vein - bilateral US.doppler
48692-8|Lower extremity vein - left US
39432-0|Lower extremity vein - left US.doppler
48691-0|Lower extremity vein - right US
39443-7|Lower extremity vein - right US.doppler
36079-2|Lower extremity veins MRI angiogram
69385-3|Lower extremity veins - bilateral US
36784-7|Lower extremity veins - left MRI angiogram
69392-9|Lower extremity veins - left US
36785-4|Lower extremity veins - right MRI angiogram
42461-4|Lower extremity vessel graft - left US.doppler
42462-2|Lower extremity vessel graft - right US.doppler
30874-2|Lower extremity vessels MRI angiogram
44174-1|Lower extremity vessels US.doppler
35974-5|Lower extremity vessels - bilateral MRI angiogram
39422-1|Lower extremity vessels - bilateral US.doppler
36795-3|Lower extremity vessels - left MRI angiogram
39431-2|Lower extremity vessels - left US.doppler
36796-1|Lower extremity vessels - right MRI angiogram
39442-9|Lower extremity vessels - right US.doppler
35973-7|Lower extremity - bilateral CT
35975-2|Lower extremity - bilateral MRI
38013-9|Lower extremity - bilateral US
24687-6|Lower Extremity Joint MRI
26227-9|Lower extremity joint - bilateral MRI
26228-7|Lower extremity joint - left MRI
26229-5|Lower extremity joint - right MRI
35976-0|Lower extremity - left CT
35978-6|Lower extremity - left MRI
38040-2|Lower extremity - left US
35977-8|Lower extremity - left X-ray tomograph
35979-4|Lower extremity - right CT
35980-2|Lower extremity - right MRI
38051-9|Lower extremity - right US
37766-3|Lower extremity - right X-ray tomograph
36074-3|Lower leg CT
24821-1|Lower leg MRI
43513-1|Lower leg vessels - left MRI angiogram
43556-0|Lower leg vessels - right MRI angiogram
42696-5|Lower leg - bilateral MRI
36075-0|Lower leg - left MRI
36076-8|Lower leg - right MRI
30866-8|Lumbar plexus MRI
57822-9|Lung PET
36047-9|Mandible CT
36048-7|Mandible X-ray tomograph
38043-6|Mastoid US
36776-3|Mastoid X-ray tomograph
46298-6|Mastoid - bilateral CT
36050-3|Maxilla CT
36049-5|Maxilla and Mandible CT
37234-2|Mediastinum MRI
38044-4|Mediastinum US
37233-4|Mediastinum X-ray tomograph
69394-5|Mesenteric artery US
69211-1|Nasal bones MRI
37606-1|Nasal bones X-ray tomograph
30860-1|Nasopharynx MRI
24835-1|Nasopharynx and Neck CT
36051-1|Neck CT
24839-3|Neck MRI
24842-7|Neck US
36788-8|Neck veins MRI angiogram
36085-9|Neck vessels MRI angiogram
44175-8|Neck vessels US.doppler
30857-7|Nerves cranial MRI
41807-9|Orbit CT
36777-1|Orbit MRI
36802-7|Orbit vessels MRI angiogram
24848-4|Orbit - bilateral CT
37611-1|Orbit - bilateral X-ray tomograph
38836-3|Orbit - left MRI
36778-9|Orbit - right MRI
42303-8|Orbit and Face MRI
43530-5|Orbit and Face and Neck MRI
43455-5|Oropharynx MRI
39502-0|Ovarian vessels US.doppler
36779-7|Ovary MRI
69390-3|Ovary US
43506-5|Ovary - bilateral MRI
24857-5|Pancreas CT
36052-9|Pancreas MRI
24859-1|Pancreas US
39509-5|Pancreas transplant US
36053-7|Parathyroid MRI
38045-1|Parathyroid US
37223-5|Parotid gland CT
37224-3|Parotid gland MRI
38138-4|Parotid gland US
24865-8|Pelvis CT
24867-4|Pelvis MRI
24869-0|Pelvis US
37632-7|Pelvis X-ray tomograph
36789-6|Pelvis veins MRI angiogram
30867-6|Pelvis vessels MRI angiogram
24870-8|Pelvis vessels US.doppler
24872-4|Pelvis and Hip MRI
26259-2|Pelvis and Hip - bilateral MRI
26260-0|Pelvis and Hip - left MRI
26261-8|Pelvis and Hip - right MRI
38140-0|Penis US
38139-2|Penis vessels US
24877-3|Petrous bone CT
36932-2|Pituitary and Sella turcica CT
24880-7|Pituitary and Sella turcica MRI
24881-5|Popliteal space US
26262-6|Popliteal space - bilateral US
26263-4|Popliteal space - left US
26264-2|Popliteal space - right US
36077-6|Portal vein MRI angiogram
69284-8|Portal vein and Hepatic vein US.doppler
36055-2|Posterior fossa CT
36056-0|Posterior fossa MRI
36057-8|Prostate CT
30675-3|Prostate MRI
24884-9|Prostate US
43445-6|Pulmonary system CT
43454-8|Pulmonary system MRI
36803-5|Pulmonary vessels MRI angiogram
24892-2|Rectum US
69294-7|Renal artery US
39435-3|Renal artery US.doppler
36078-4|Renal vein MRI angiogram
30868-4|Renal vessels MRI angiogram
69295-4|Renal vessels US
39426-2|Renal vessels US.doppler
36804-3|Renal vessels - bilateral MRI angiogram
39419-7|Renal vessels - bilateral US.doppler
30619-1|Sacroiliac Joint CT
36031-3|Sacroiliac Joint MRI
36058-6|Sacrum CT
36059-4|Sacrum MRI
38053-5|Sacrum US
37653-3|Sacrum X-ray tomograph
69116-2|Sacrum and Coccyx CT
36060-2|Sacrum and Coccyx MRI
36933-0|Salivary gland MRI
69298-8|Salivary gland US
69117-0|Scapula CT
36061-0|Scapula MRI
36073-5|Scrotum and Testicle MRI
25002-7|Scrotum and Testicle US
48742-1|Scrotum and Testicle US.doppler
26271-7|Scrotum and Testicle - bilateral US
26272-5|Scrotum and Testicle - left US
26273-3|Scrotum and Testicle - right US
42437-4|Sella turcica X-ray tomograph
36062-8|Shoulder CT
24905-2|Shoulder MRI
24907-8|Shoulder US
37850-5|Shoulder X-ray tomograph
36805-0|Shoulder vessels MRI angiogram
36806-8|Shoulder vessels - left MRI angiogram
36807-6|Shoulder vessels - right MRI angiogram
36063-6|Shoulder - bilateral CT
26266-7|Shoulder - bilateral MRI
26265-9|Shoulder - bilateral US
36064-4|Shoulder - left CT
26268-3|Shoulder - left MRI
26267-5|Shoulder - left US
36065-1|Shoulder - left X-ray tomograph
36066-9|Shoulder - right CT
26270-9|Shoulder - right MRI
26269-1|Shoulder - right US
37811-7|Shoulder - right X-ray tomograph
30588-8|Sinuses CT
24914-4|Sinuses MRI
37866-1|Sinuses X-ray tomograph
37874-5|Skull X-ray tomograph
37495-9|Skull.base CT
37497-5|Spine vessels MRI angiogram
24932-6|Spine Cervical CT
24935-9|Spine Cervical MRI
70926-1|Spine Cervical US
36068-5|Spine Cervical X-ray tomograph
43457-1|Spine Cervical and Spine Thoracic MRI
42698-1|Spine Cervical and Thoracic and Lumbar MRI
24963-1|Spine Lumbar CT
24968-0|Spine Lumbar MRI
69393-7|Spine Lumbar US
36069-3|Spine Lumbar X-ray tomograph
37232-6|Spine Lumbosacral Junction CT
24978-9|Spine Thoracic CT
24980-5|Spine Thoracic MRI
70927-9|Spine Thoracic US
37911-5|Spine Thoracic X-ray tomograph
49565-5|Thoracic Spine vessels MRI angiogram
24988-8|Spleen CT
36070-1|Spleen MRI
24990-4|Spleen US
37225-0|Sternoclavicular Joint CT
36071-9|Sternum CT
36072-7|Sternum MRI
37885-1|Sternum X-ray tomograph
36782-1|Subclavian artery MRI angiogram
38131-9|Subclavian vessels - bilateral US
46359-6|Superior mesenteric vessels MRI angiogram
44235-0|Superior mesenteric vessels US.doppler
42468-9|Surgical specimen US
38059-2|Talus CT
36773-0|Temporal bone CT
37226-8|Temporomandibular joint CT
24999-5|Temporomandibular joint MRI
30719-9|Temporomandibular joint X-ray tomograph
37228-4|Temporomandibular joint - bilateral MRI
37227-6|Temporomandibular joint - bilateral X-ray tomograph
37230-0|Temporomandibular joint - left MRI
37229-2|Temporomandibular joint - left X-ray tomograph
37231-8|Temporomandibular joint - right MRI
37819-0|Temporomandibular joint - right X-ray tomograph
39446-0|Testicle vessels US.doppler
24702-3|Thigh MRI
26235-2|Thigh - bilateral MRI
26236-0|Thigh - left MRI
26237-8|Thigh - right MRI
36054-5|Thoracic outlet CT
24582-9|Thoracic outlet MRI
44163-4|Thoracic outlet US
26211-3|Thoracic outlet - bilateral MRI
26212-1|Thoracic outlet - left MRI
26213-9|Thoracic outlet - right MRI
43507-3|Thymus gland MRI
42300-4|Thyroid MRI
25010-0|Thyroid US
37898-4|Tibia and Fibula X-ray tomograph
30888-2|Tibioperoneal vessels MRI angiogram
36780-5|Toe MRI
69285-5|Umbilical artery US.doppler
39508-7|Umbilical vessels US.doppler
36023-0|Upper arm CT
36025-5|Upper arm MRI
36026-3|Upper arm - bilateral CT
69180-8|Upper arm - bilateral MRI
36027-1|Upper arm - left CT
36028-9|Upper arm - left MRI
36029-7|Upper arm - right CT
36030-5|Upper arm - right MRI
35981-0|Upper extremity CT
24688-4|Upper extremity MRI
30710-8|Upper extremity US
37923-0|Upper extremity X-ray tomograph
48448-5|Upper extremity artery US
39447-8|Upper extremity artery US.doppler
38014-7|Upper extremity artery - bilateral US
39423-9|Upper extremity artery - bilateral US.doppler
41833-5|Upper extremity artery - left US
39500-4|Upper extremity artery - left US.doppler
41814-5|Upper extremity artery - right US
39506-1|Upper extremity artery - right US.doppler
30882-5|Upper extremity vein US.doppler
48690-2|Upper extremity vein - bilateral US
39496-5|Upper extremity vein - bilateral US.doppler
48689-4|Upper extremity vein - left US
39501-2|Upper extremity vein - left US.doppler
48688-6|Upper extremity vein - right US
39507-9|Upper extremity vein - right US.doppler
36080-0|Upper extremity veins MRI angiogram
69395-2|Upper extremity veins US
36786-2|Upper extremity veins - left MRI angiogram
36787-0|Upper extremity veins - right MRI angiogram
46385-1|Upper extremity vessel graft US.doppler
44236-8|Upper extremity vessel graft - bilateral US.doppler
42475-4|Upper extremity vessel graft - left US.doppler
42476-2|Upper extremity vessel graft - right US.doppler
36084-2|Upper extremity vessels MRI angiogram
39448-6|Upper extremity vessels US.doppler
46379-4|Upper extremity vessels - bilateral US.doppler
36797-9|Upper extremity vessels - left MRI angiogram
39433-8|Upper extremity vessels - left US.doppler
36798-7|Upper extremity vessels - right MRI angiogram
39444-5|Upper extremity vessels - right US.doppler
26232-9|Upper extremity - bilateral MRI
30875-9|Upper extremity .joint MRI
36774-8|Upper extremity joint - left MRI
36775-5|Upper extremity joint - right MRI
35982-8|Upper extremity - left CT
26233-7|Upper extremity - left MRI
38041-0|Upper extremity - left US
35983-6|Upper extremity - right CT
26234-5|Upper extremity - right MRI
38052-7|Upper extremity - right US
25019-1|Urinary bladder US
42301-2|Uterus MRI
30705-8|Uterus and Fallopian tubes US
39036-9|Vein US
39525-1|Vein US.doppler
39030-2|Vein - bilateral US
36783-9|Veins MRI angiogram
69222-8|Vena cava MRI
36081-8|Vena cava MRI angiogram
36083-4|Inferior vena cava MRI
36082-6|Inferior vena cava MRI angiogram
36790-4|Vena cava.inferior and Lower extremity veins MRI angiogram
39445-2|Vessels US.doppler
38054-3|Visceral artery US
37428-0|Wrist CT
25033-2|Wrist MRI
25036-5|Wrist US
37932-1|Wrist X-ray tomograph
37430-6|Wrist - bilateral CT
26277-4|Wrist - bilateral MRI
26278-2|Wrist - bilateral US
37429-8|Wrist - bilateral X-ray tomograph
37431-4|Wrist - left CT
26279-0|Wrist - left MRI
26280-8|Wrist - left US
37432-2|Wrist - left X-ray tomograph
69209-5|Wrist - left and Hand - left MRI
37433-0|Wrist - right CT
26281-6|Wrist - right MRI
26282-4|Wrist - right US
37644-2|Wrist - right X-ray tomograph
69219-4|Wrist - right and Hand - right MRI
36008-1|Wrist and Hand MRI
25045-6|Unspecified body region CT
25040-7|Unspecified body region CT 3D
25056-3|Unspecified body region MRI
44136-0|Unspecified body region PET
25061-3|Unspecified body region US
25071-2|Unspecified body region X-ray tomograph
46375-2|Artery US
39523-6|Artery US.doppler
44229-3|Bones CT
28576-7|Joint MRI
39453-6|Tendon US
36957-9|Facial bones and Maxilla CT and 3D reconstruction
37294-6|Head CT and 3D reconstruction
41804-6|Unspecified body region CT and 3D reconstruction
39043-5|Unspecified body region MRI and 3D reconstruction
44165-9|Unspecified body region US and 3D reconstruction
58745-1|Coronary arteries CT angiogram and 3D reconstruction W contrast IV
59255-0|Left atrium and Pulmonary veins CT angiogram and 3D reconstruction W contrast IV
69082-6|Head CT and 3D reconstruction WO contrast
37295-3|Femur and Hip CT and anteversion measurement
72830-3|Extremity arteries - bilateral US.doppler Multisection and physiologic artery study
72832-9|Extremity arteries - bilateral US.doppler Multisection and physiologic artery study at rest & W exercise
39879-2|Bone SPECT 1 phase
39881-8|Bone SPECT 3 phase whole body
30760-3|Kidney - bilateral X-ray tomograph 3 views W contrast IV
25055-5|Unspecified body region MRI additional sequence
39408-0|Spine Thoracic X-ray tomograph AP
39862-8|Heart SPECT blood pool at rest and W radionuclide IV
47378-5|Liver SPECT blood pool
37435-5|Temporomandibular joint MRI cine
42693-2|Urinary Bladder and Urethra MRI cine
39140-9|Heart MRI cine for blood flow velocity mapping
44126-1|Heart MRI cine for blood flow velocity mapping W contrast IV
42386-3|Brain MRI cine for CSF flow
42387-1|Unspecified body region MRI cine for CSF flow
37434-8|Heart MRI cine for function
46300-0|Sinuses CT coronal
72139-9|Breast - bilateral FFD mammogram-tomosynthesis diagnostic
72138-1|Breast - left FFD mammogram-tomosynthesis diagnostic
72137-3|Breast - right FFD mammogram-tomosynthesis diagnostic
37436-3|Brain MRI diffusion weighted
43555-2|Ankle - left MRI dynamic W contrast IV
43449-8|Ankle - right MRI dynamic W contrast IV
37437-1|Breast MRI dynamic W contrast IV
36114-7|Breast - bilateral MRI dynamic W contrast IV
43450-6|Elbow - left MRI dynamic W contrast IV
43451-4|Elbow - right MRI dynamic W contrast IV
46394-3|Head CT dynamic W contrast IV
43452-2|Knee - left MRI dynamic W contrast IV
43453-0|Knee - right MRI dynamic W contrast IV
37438-9|Pituitary and Sella turcica CT dynamic W contrast IV
43527-1|Unspecified body region CT dynamic W contrast IV
39637-4|Brain SPECT flow
43655-0|Liver SPECT flow
43652-7|Liver and Spleen SPECT flow
69235-0|Scrotum and Testicle SPECT flow
43670-9|Spleen SPECT flow
43673-3|Thyroid SPECT flow
43662-6|Renal vessels SPECT flow W Tc-99m glucoheptonate IV
39684-6|SPECT for abscess W GA-67 IV
39811-5|SPECT for abscess
39141-7|Bone marrow MRI for blood flow
39656-4|Heart SPECT for infarct
39654-9|Heart SPECT for infarct W Tc-99m PYP IV
39655-6|Heart SPECT for infarct W Tc-99m Sestamibi IV
39675-4|SPECT for infection W GA-67 IV
72251-2|Chest vessels CT Multisection for pulmonary embolus
24889-8|Pylorus US for pyloric stenosis
36934-8|Heart CT for scoring
36935-5|Heart CT for scoring W contrast IV
43446-4|CT for tumor whole body
69237-6|SPECT for tumor whole body
39678-8|SPECT for tumor W GA-67 IV
39748-9|SPECT for tumor W Tc-99m Sestamibi IV
42292-3|SPECT for tumor W Tl-201 IV
46395-0|Heart SPECT gated and ejection fraction at rest and W stress and W radionuclide IV
39913-9|Heart SPECT gated and ejection fraction
39918-8|Heart SPECT gated and wall motion
46396-8|Heart SPECT gated at rest and W Tc-99m Sestamibi IV
39916-2|Heart SPECT gated
39930-3|Heart SPECT gated W stress and W radionuclide IV
37439-7|Chest CT high resolution
37440-5|Chest CT high resolution W contrast IV
37441-3|Chest CT high resolution WO contrast
39409-8|Spine Thoracic X-ray tomograph lateral
36086-7|Abdomen CT limited
30704-1|Abdomen US limited
38047-7|Abdomen retroperitoneum US limited
43572-7|Abdominal vessels US.doppler limited
38011-3|Aorta US limited
69280-6|Bladder US limited
24599-3|Breast US limited
26286-5|Breast - bilateral US limited
26288-1|Breast - left US limited
26290-7|Breast - right US limited
38015-4|Carotid artery US limited
42149-5|Carotid artery - left US limited
42151-1|Carotid artery - right US limited
36089-1|Chest CT limited
69281-4|Chest US limited
36090-9|Extremity CT limited
39526-9|Extremity US limited
46301-8|Extremity vein - bilateral US.doppler limited
39424-7|Extremity vessels US.doppler limited
62451-0|Extremity - left US limited
62452-8|Extremity - right US limited
69286-3|Eye US limited
36937-1|Facial bones and Maxilla CT limited
38020-4|Gallbladder US limited
36087-5|Head CT limited
38034-5|Head US limited
36808-4|Head vessels MRI angiogram limited
39044-3|Head vessels US.doppler limited
36091-7|Heart MRI limited
42707-0|Heart US limited
36092-5|Hip CT limited
43776-4|Iliac artery US.doppler limited
42150-3|Iliac graft US.doppler limited
36088-3|Internal auditory canal MRI limited
38035-2|Kidney US limited
69300-2|Kidney transplant US limited
41812-9|Lower extremity artery US limited
38042-8|Lower extremity artery US.doppler limited
39430-4|Lower extremity vessels - left US.doppler limited
39441-1|Lower extremity vessels - right US.doppler limited
36093-3|Lower Extremity Joint MRI limited
38039-4|Lower extremity - left US limited
38050-1|Lower extremity - right US limited
44116-2|Mandible CT limited
48461-8|Neck MRI limited
69212-9|Pelvis MRI limited
38046-9|Pelvis US limited
42152-9|Pelvis vessels US.doppler limited
44173-3|Peripheral artery US limited
39436-1|Renal vessels US.doppler limited
69299-6|Scrotum and Testicle US limited
24913-6|Sinuses CT limited
41813-7|Upper extremity artery US limited
38143-4|Upper extremity artery US.doppler limited
46302-6|Upper extremity artery - bilateral US.doppler limited
44237-6|Upper extremity vessel graft - bilateral US.doppler limited
46303-4|Upper extremity vessels US.doppler limited
36094-1|Upper extremity .joint MRI limited
39045-0|Vein US limited
39524-4|Vein US.doppler limited
25039-9|Unspecified body region CT limited
48460-0|Unspecified body region MRI limited
69282-2|Unspecified body region US.doppler limited
72831-1|Extremity arteries - bilateral US.doppler Multisection limited and physiologic artery study
44127-9|Heart MRI limited cine for function
39046-8|Pelvis CT limited pelvimetry WO contrast
36102-2|Abdomen CT limited W and WO contrast IV
36095-8|Abdomen CT limited W contrast IV
36096-6|Brain MRI limited W contrast IV
69096-6|Chest CT limited W contrast IV
36098-2|Pelvis CT limited W contrast IV
36099-0|Spine Cervical CT limited W contrast IV
36100-6|Spine Lumbar MRI limited W contrast IV
36101-4|Spine Thoracic MRI limited W contrast IV
36097-4|Upper extremity CT limited W contrast IV
39681-2|SPECT limited W GA-67 IV
39813-1|Bone SPECT limited
39821-4|Bone marrow SPECT limited
36103-0|Abdomen CT limited WO contrast
36105-5|Brain MRI limited WO contrast
47366-0|Chest CT limited WO contrast
36938-9|Facial bones and Maxilla CT limited WO contrast
36104-8|Head CT limited WO contrast
36106-3|Lower extremity CT limited WO contrast
36107-1|Lower extremity joint - left MRI limited WO contrast
38769-6|Lower extremity joint - right MRI limited WO contrast
36108-9|Pelvis CT limited WO contrast
46304-2|Sinuses CT limited WO contrast
36109-7|Spine Cervical CT limited WO contrast
36110-5|Spine Lumbar CT limited WO contrast
36111-3|Spine Lumbar MRI limited WO contrast
36112-1|Spine Thoracic MRI limited WO contrast
39905-5|Bone SPECT multiple areas
39906-3|Bone marrow SPECT multiple areas
39527-7|Unspecified body region US of foreign body
49569-7|Heart SPECT perfusion and wall motion at rest and W stress and W Tl-201 IV and W Tc-99m Sestamibi IV
43659-2|Heart SPECT perfusion qualitative at rest and W radionuclide IV
39725-7|Heart SPECT perfusion at rest and W adenosine and W Tl-201 IV
39718-2|Heart SPECT perfusion at rest and W radionuclide IV
39724-0|Heart SPECT perfusion at rest and W stress and W radionuclide IV
39723-2|Heart SPECT perfusion at rest and W stress and W Tl-201 IV
49568-9|Heart SPECT perfusion at rest and W stress and W Tl-201 IV and W Tc-99m Sestamibi IV
39729-9|Heart SPECT perfusion at rest and W Tl-201 IV
39700-0|Heart SPECT perfusion W adenosine and W radionuclide IV
49567-1|Heart SPECT perfusion W adenosine and W Tc-99m Sestamibi IV
39142-5|Head CT perfusion W contrast IV
39712-5|Heart SPECT perfusion
39734-9|Heart SPECT perfusion W stress and W radionuclide IV
39736-4|Heart SPECT perfusion W stress and W Tc-99m Sestamibi IV
39710-9|Heart SPECT perfusion W Tc-99m Sestamibi IV
39711-7|Heart SPECT perfusion W Tl-201 IV
38060-0|Spine.lumbosacral+Cervical+Thoracic MRI sagittal
25052-2|Unspecified body region CT sagittal and coronal
25050-6|Unspecified body region CT 3D sagittal and coronal disarticulation
42132-1|Breast US screening
72142-3|Breast - bilateral FFD mammogram-tomosynthesis screening
72141-5|Breast - left FFD mammogram-tomosynthesis screening
72140-7|Breast - right FFD mammogram-tomosynthesis screening
37442-1|Brain MRI spectroscopy
37443-9|Unspecified body region MRI spectroscopy
70929-5|Spine Cervical CT stereotactic
70928-7|Spine Lumbar CT stereotactic
70930-3|Spine Thoracic CT stereotactic
36940-5|Unspecified body region CT stereotactic
42455-6|Pelvis US transabdominal and transvaginal
24677-7|Pelvis US transvaginal
42390-5|Transvaginal MRI
39838-8|Lung SPECT ventilation and perfusion W radionuclide inhaled and W radionuclide IV
39898-2|Lung SPECT ventilation W radionuclide aerosol inhaled
39872-7|Heart SPECT wall motion
46305-9|CT whole body
46358-8|MRI whole body
44139-4|PET whole body
46306-7|CT whole body W contrast IV
39680-4|SPECT whole body W GA-67 IV
39816-4|Bone SPECT whole body
39825-5|Bone marrow SPECT whole body
41837-6|SPECT whole body W Tc-99m Arcitumomab IV
39658-0|Heart SPECT at rest and W radionuclide IV
39662-2|Heart SPECT at rest and W stress and W Tc-99m Sestamibi IV
49566-3|Heart SPECT at rest and W Tc-99m Sestamibi IV
30711-6|Hip US developmental joint assessment
24732-0|Head US during surgery
30706-6|Liver US during surgery
30701-7|Unspecified body region US during surgery
69388-7|Urinary bladder US post void
69086-7|Aorta CT W and WO contrast
69108-9|Pulmonary vessels CT angiogram W and WO contrast
69085-9|Renal vessels CT angiogram W and WO contrast
69207-9|Hip - left MRI W and WO contrast intraarticular
69217-8|Hip - right MRI W and WO contrast intraarticular
69208-7|Shoulder - left MRI W and WO contrast intraarticular
69218-6|Shoulder - right MRI W and WO contrast intraarticular
48450-1|Spine Cervical MRI W and WO contrast IT
44114-7|Spine Lumbar CT W and WO contrast IT
48452-7|Spine Lumbar MRI W and WO contrast IT
44113-9|Spine Thoracic CT W and WO contrast IT
48441-0|Spine Thoracic MRI W and WO contrast IT
36267-3|Abdomen CT W and WO contrast IV
24557-1|Abdomen MRI W and WO contrast IV
48743-9|Abdomen retroperitoneum CT W and WO contrast IV
42274-1|Abdomen and Pelvis CT W and WO contrast IV
36846-4|Abdominal veins MRI angiogram W and WO contrast IV
30805-6|Abdominal vessels CT angiogram W and WO contrast IV
36855-5|Abdominal vessels MRI angiogram W and WO contrast IV
36950-4|Adrenal gland CT W and WO contrast IV
36951-2|Adrenal gland MRI W and WO contrast IV
36268-1|Ankle CT W and WO contrast IV
24539-9|Ankle MRI W and WO contrast IV
26187-5|Ankle - bilateral MRI W and WO contrast IV
36269-9|Ankle - left CT W and WO contrast IV
26188-3|Ankle - left MRI W and WO contrast IV
36270-7|Ankle - right CT W and WO contrast IV
26189-1|Ankle - right MRI W and WO contrast IV
44131-1|Aorta MRI angiogram W and WO contrast IV
36271-5|Aorta abdominal CT W and WO contrast IV
36273-1|Aorta abdominal MRI W and WO contrast IV
36272-3|Aorta abdominal MRI angiogram W and WO contrast IV
36274-9|Aorta thoracic MRI angiogram W and WO contrast IV
30806-4|Aorta and Femoral artery - bilateral CT angiogram W and WO contrast IV
46360-4|Aortic arch MRI angiogram W and WO contrast IV
43509-9|Axilla - left MRI W and WO contrast IV
43511-5|Axilla - right MRI W and WO contrast IV
36944-7|Biliary ducts and Pancreatic duct MRI W and WO contrast IV
24587-8|Brain MRI W and WO contrast IV
48694-4|Brain.temporal MRI W and WO contrast IV
43769-9|Brain and Internal auditory canal MRI W and WO contrast IV
42392-1|Brain and Pituitary and Sella turcica MRI W and WO contrast IV
36276-4|Breast MRI W and WO contrast IV
69189-9|Breast implant MRI W and WO contrast IV
69166-7|Breast implant - bilateral MRI W and WO contrast IV
38870-2|Breast implant - left MRI W and WO contrast IV
38062-6|Breast implant - right MRI W and WO contrast IV
36277-2|Breast - bilateral MRI W and WO contrast IV
36278-0|Breast - left MRI W and WO contrast IV
36279-8|Breast - right MRI W and WO contrast IV
43528-9|Breast - unilateral MRI W and WO contrast IV
36358-0|Calcaneus CT W and WO contrast IV
36280-6|Calcaneus - left CT W and WO contrast IV
36281-4|Calcaneus - right CT W and WO contrast IV
36856-3|Carotid vessel MRI angiogram W and WO contrast IV
30598-7|Chest CT W and WO contrast IV
36283-0|Chest MRI W and WO contrast IV
36848-0|Chest veins MRI angiogram W and WO contrast IV
30804-9|Chest vessels CT angiogram W and WO contrast IV
36420-8|Chest vessels MRI angiogram W and WO contrast IV
42277-4|Chest and Abdomen CT W and WO contrast IV
36284-8|Chest and Abdomen MRI W and WO contrast IV
72252-0|Chest and Abdomen and Pelvis CT W and WO contrast IV
69161-8|Circle of Willis MRI angiogram W and WO contrast IV
42299-8|Clavicle MRI W and WO contrast IV
48455-0|Clavicle - left MRI W and WO contrast IV
48454-3|Clavicle - right MRI W and WO contrast IV
36285-5|Elbow CT W and WO contrast IV
24675-1|Elbow MRI W and WO contrast IV
26193-3|Elbow - bilateral MRI W and WO contrast IV
36286-3|Elbow - left CT W and WO contrast IV
26194-1|Elbow - left MRI W and WO contrast IV
36287-1|Elbow - right CT W and WO contrast IV
26195-8|Elbow - right MRI W and WO contrast IV
42268-3|Extremity CT W and WO contrast IV
24694-2|Face MRI W and WO contrast IV
30803-1|Facial bones and Maxilla CT W and WO contrast IV
36338-2|Femur CT W and WO contrast IV
36339-0|Femur - left CT W and WO contrast IV
36340-8|Femur - right CT W and WO contrast IV
69194-9|Finger MRI W and WO contrast IV
69204-6|Finger - left MRI W and WO contrast IV
69214-5|Finger - right MRI W and WO contrast IV
36341-6|Foot CT W and WO contrast IV
30682-9|Foot MRI W and WO contrast IV
36342-4|Foot - bilateral MRI W and WO contrast IV
36343-2|Foot - left CT W and WO contrast IV
36344-0|Foot - left MRI W and WO contrast IV
36345-7|Foot - right CT W and WO contrast IV
36346-5|Foot - right MRI W and WO contrast IV
36347-3|Forearm CT W and WO contrast IV
30684-5|Forearm MRI W and WO contrast IV
69174-1|Forearm - bilateral MRI W and WO contrast IV
36348-1|Forearm - left CT W and WO contrast IV
36349-9|Forearm - left MRI W and WO contrast IV
36350-7|Forearm - right CT W and WO contrast IV
36351-5|Forearm - right MRI W and WO contrast IV
36352-3|Hand CT W and WO contrast IV
30686-0|Hand MRI W and WO contrast IV
69177-4|Hand - bilateral MRI W and WO contrast IV
36353-1|Hand - left CT W and WO contrast IV
36354-9|Hand - left MRI W and WO contrast IV
36355-6|Hand - right CT W and WO contrast IV
36356-4|Hand - right MRI W and WO contrast IV
24726-2|Head CT W and WO contrast IV
24729-6|Head CT cine W and WO contrast IV
36847-2|Head veins MRI angiogram W and WO contrast IV
30593-8|Head vessels CT angiogram W and WO contrast IV
36857-1|Head vessels MRI angiogram W and WO contrast IV
36357-2|Heart MRI W and WO contrast IV
36359-8|Hip CT W and WO contrast IV
30688-6|Hip MRI W and WO contrast IV
36360-6|Hip - bilateral CT W and WO contrast IV
36361-4|Hip - bilateral MRI W and WO contrast IV
36362-2|Hip - left CT W and WO contrast IV
36363-0|Hip - left MRI W and WO contrast IV
36364-8|Hip - right CT W and WO contrast IV
36365-5|Hip - right MRI W and WO contrast IV
36282-2|Internal auditory canal CT W and WO contrast IV
30659-7|Internal auditory canal MRI W and WO contrast IV
24740-3|Internal auditory canal and Posterior fossa MRI W and WO contrast IV
43768-1|Kidney CT W and WO contrast IV
43775-6|Kidney MRI W and WO contrast IV
36377-0|Kidney - bilateral CT W and WO contrast IV
36378-8|Kidney - bilateral MRI W and WO contrast IV
24784-1|Kidney - bilateral X-ray tomograph W and WO contrast IV
36379-6|Knee CT W and WO contrast IV
24803-9|Knee MRI W and WO contrast IV
38837-1|Knee vessels - left MRI angiogram W and WO contrast IV
36862-1|Knee vessels - right MRI angiogram W and WO contrast IV
26199-0|Knee - bilateral MRI W and WO contrast IV
36380-4|Knee - left CT W and WO contrast IV
26200-6|Knee - left MRI W and WO contrast IV
36381-2|Knee - right CT W and WO contrast IV
26201-4|Knee - right MRI W and WO contrast IV
36382-0|Larynx MRI W and WO contrast IV
30612-6|Liver CT W and WO contrast IV
30670-4|Liver MRI W and WO contrast IV
36288-9|Lower extremity CT W and WO contrast IV
39291-0|Lower extremity MRI W and WO contrast IV
36416-6|Lower extremity veins MRI angiogram W and WO contrast IV
36849-8|Lower extremity veins - left MRI angiogram W and WO contrast IV
36850-6|Lower extremity veins - right MRI angiogram W and WO contrast IV
30807-2|Lower extremity vessels CT angiogram W and WO contrast IV
44128-7|Lower extremity vessels MRI angiogram W and WO contrast IV
46308-3|Lower extremity vessels - left CT angiogram W and WO contrast IV
36858-9|Lower extremity vessels - left MRI angiogram W and WO contrast IV
46307-5|Lower extremity vessels - right CT angiogram W and WO contrast IV
36859-7|Lower extremity vessels - right MRI angiogram W and WO contrast IV
36289-7|Lower extremity - bilateral MRI W and WO contrast IV
36371-3|Lower Extremity Joint MRI W and WO contrast IV
36372-1|Lower extremity joint - left MRI W and WO contrast IV
36373-9|Lower extremity joint - right MRI W and WO contrast IV
36290-5|Lower extremity - left CT W and WO contrast IV
36291-3|Lower extremity - left MRI W and WO contrast IV
36292-1|Lower extremity - right CT W and WO contrast IV
36333-3|Lower extremity - right MRI W and WO contrast IV
36408-3|Lower leg CT W and WO contrast IV
30870-0|Lower leg MRI W and WO contrast IV
42697-3|Lower leg - bilateral MRI W and WO contrast IV
36409-1|Lower leg - left CT W and WO contrast IV
36410-9|Lower leg - left MRI W and WO contrast IV
36411-7|Lower leg - right CT W and WO contrast IV
36412-5|Lower leg - right MRI W and WO contrast IV
36383-8|Mandible CT W and WO contrast IV
37272-2|Mediastinum MRI W and WO contrast IV
48443-6|Nasopharynx CT W and WO contrast IV
36384-6|Nasopharynx MRI W and WO contrast IV
30586-2|Neck CT W and WO contrast IV
24840-1|Neck MRI W and WO contrast IV
36853-0|Neck veins MRI angiogram W and WO contrast IV
30594-6|Neck vessels CT angiogram W and WO contrast IV
36423-2|Neck vessels MRI angiogram W and WO contrast IV
48451-9|Orbit CT W and WO contrast IV
36842-3|Orbit MRI W and WO contrast IV
43458-9|Orbit vessels MRI angiogram W and WO contrast IV
24849-2|Orbit - bilateral CT W and WO contrast IV
24851-8|Orbit - bilateral MRI W and WO contrast IV
36843-1|Orbit - left MRI W and WO contrast IV
36844-9|Orbit - right MRI W and WO contrast IV
39029-4|Orbit and Face MRI W and WO contrast IV
46310-9|Orbit and Face and Neck MRI W and WO contrast IV
36845-6|Ovary MRI W and WO contrast IV
30614-2|Pancreas CT W and WO contrast IV
36385-3|Pancreas MRI W and WO contrast IV
46311-7|Parotid gland CT W and WO contrast IV
37265-6|Parotid gland MRI W and WO contrast IV
30616-7|Pelvis CT W and WO contrast IV
30674-6|Pelvis MRI W and WO contrast IV
36854-8|Pelvis veins MRI angiogram W and WO contrast IV
30623-3|Pelvis vessels CT angiogram W and WO contrast IV
36863-9|Pelvis vessels MRI angiogram W and WO contrast IV
30672-0|Pelvis and Hip MRI W and WO contrast IV
36835-7|Petrous bone CT W and WO contrast IV
24904-5|Pituitary and Sella turcica CT W and WO contrast IV
24879-9|Pituitary and Sella turcica MRI W and WO contrast IV
36414-1|Portal vein MRI angiogram W and WO contrast IV
36387-9|Posterior fossa CT W and WO contrast IV
36388-7|Posterior fossa MRI W and WO contrast IV
36389-5|Prostate MRI W and WO contrast IV
36275-6|Renal artery MRI angiogram W and WO contrast IV
36415-8|Renal vein MRI angiogram W and WO contrast IV
44134-5|Renal vessels MRI angiogram W and WO contrast IV
36375-4|Sacroiliac Joint CT W and WO contrast IV
36376-2|Sacroiliac Joint MRI W and WO contrast IV
36390-3|Sacrum CT W and WO contrast IV
36391-1|Sacrum MRI W and WO contrast IV
36392-9|Sacrum and Coccyx MRI W and WO contrast IV
36393-7|Scapula - left MRI W and WO contrast IV
36394-5|Scapula - right MRI W and WO contrast IV
36406-7|Scrotum and Testicle MRI W and WO contrast IV
36395-2|Shoulder CT W and WO contrast IV
24906-0|Shoulder MRI W and WO contrast IV
36864-7|Shoulder vessels - left MRI angiogram W and WO contrast IV
36865-4|Shoulder vessels - right MRI angiogram W and WO contrast IV
26202-2|Shoulder - bilateral MRI W and WO contrast IV
36396-0|Shoulder - left CT W and WO contrast IV
26203-0|Shoulder - left MRI W and WO contrast IV
36397-8|Shoulder - right CT W and WO contrast IV
26204-8|Shoulder - right MRI W and WO contrast IV
36398-6|Sinuses CT W and WO contrast IV
30663-9|Sinuses MRI W and WO contrast IV
44111-3|Skull.base CT W and WO contrast IV
69220-2|Skull.base MRI W and WO contrast IV
37277-1|Spinal vein MRI angiogram W and WO contrast IV
37505-5|Spine vessels MRI angiogram W and WO contrast IV
36401-8|Spine Cervical CT W and WO contrast IV
24937-5|Spine Cervical MRI W and WO contrast IV
37506-3|Cervical Spine vessels MRI angiogram W and WO contrast IV
43456-3|Spine Cervical and Spine Thoracic MRI W and WO contrast IV
30855-1|Spine Cervical and Thoracic and Lumbar MRI W and WO contrast IV
36402-6|Spine Lumbar CT W and WO contrast IV
24967-2|Spine Lumbar MRI W and WO contrast IV
37507-1|Lumbar Spine vessels MRI angiogram W and WO contrast IV
36403-4|Spine Thoracic CT W and WO contrast IV
24981-3|Spine Thoracic MRI W and WO contrast IV
37508-9|Thoracic Spine vessels MRI angiogram W and WO contrast IV
24989-6|Spleen CT W and WO contrast IV
36404-2|Spleen MRI W and WO contrast IV
37266-4|Sternoclavicular Joint CT W and WO contrast IV
36405-9|Sternum CT W and WO contrast IV
44231-9|Superior mesenteric vessels MRI angiogram W and WO contrast IV
36837-3|Temporal bone CT W and WO contrast IV
37267-2|Temporomandibular joint CT W and WO contrast IV
37268-0|Temporomandibular joint MRI W and WO contrast IV
37269-8|Temporomandibular joint - bilateral MRI W and WO contrast IV
37270-6|Temporomandibular joint - left MRI W and WO contrast IV
37271-4|Temporomandibular joint - right MRI W and WO contrast IV
24703-1|Thigh MRI W and WO contrast IV
26196-6|Thigh - bilateral MRI W and WO contrast IV
26197-4|Thigh - left MRI W and WO contrast IV
26198-2|Thigh - right MRI W and WO contrast IV
24583-7|Thoracic outlet MRI W and WO contrast IV
26190-9|Thoracic outlet - bilateral MRI W and WO contrast IV
26191-7|Thoracic outlet - left MRI W and WO contrast IV
26192-5|Thoracic outlet - right MRI W and WO contrast IV
36407-5|Thyroid MRI W and WO contrast IV
72241-3|Toes - left MRI W and WO contrast IV
72238-9|Toes - right MRI W and WO contrast IV
36366-3|Upper arm CT W and WO contrast IV
30690-2|Upper arm MRI W and WO contrast IV
69181-6|Upper arm - bilateral MRI W and WO contrast IV
36367-1|Upper arm - left CT W and WO contrast IV
36368-9|Upper arm - left MRI W and WO contrast IV
36369-7|Upper arm - right CT W and WO contrast IV
36370-5|Upper arm - right MRI W and WO contrast IV
36334-1|Upper extremity CT W and WO contrast IV
39034-4|Upper extremity MRI W and WO contrast IV
36417-4|Upper extremity veins MRI angiogram W and WO contrast IV
36851-4|Upper extremity veins - left MRI angiogram W and WO contrast IV
36852-2|Upper extremity veins - right MRI angiogram W and WO contrast IV
36421-6|Upper extremity vessels CT angiogram W and WO contrast IV
36422-4|Upper extremity vessels MRI angiogram W and WO contrast IV
46312-5|Upper extremity vessels - left CT angiogram W and WO contrast IV
36860-5|Upper extremity vessels - left MRI angiogram W and WO contrast IV
46309-1|Upper extremity vessels - right CT angiogram W and WO contrast IV
36861-3|Upper extremity vessels - right MRI angiogram W and WO contrast IV
69186-5|Upper extremity - bilateral MRI W and WO contrast IV
36374-7|Upper extremity .joint MRI W and WO contrast IV
36840-7|Upper extremity joint - left MRI W and WO contrast IV
36841-5|Upper extremity joint - right MRI W and WO contrast IV
36335-8|Upper extremity - left CT W and WO contrast IV
38831-4|Upper extremity - left MRI W and WO contrast IV
36336-6|Upper extremity - right CT W and WO contrast IV
36337-4|Upper extremity - right MRI W and WO contrast IV
36413-3|Uterus MRI W and WO contrast IV
36418-2|Inferior vena cava MRI W and WO contrast IV
36419-0|Superior vena cava MRI W and WO contrast IV
37457-9|Wrist CT W and WO contrast IV
25035-7|Wrist MRI W and WO contrast IV
26205-5|Wrist - bilateral MRI W and WO contrast IV
37458-7|Wrist - left CT W and WO contrast IV
26206-3|Wrist - left MRI W and WO contrast IV
38802-5|Wrist - right CT W and WO contrast IV
26207-1|Wrist - right MRI W and WO contrast IV
42298-0|Unspecified body region MRI W and WO contrast IV
24588-6|Brain MRI W and WO contrast IV and W anesthesia
72244-7|Pelvis MRI W and WO contrast IV and W endorectal coil
43448-0|Liver MRI W and WO ferumoxides IV
46318-2|Abdomen CT W and WO reduced contrast volume IV
46317-4|Chest CT W and WO reduced contrast volume IV
46315-8|Facial bones and Maxilla CT W and WO reduced contrast volume IV
46316-6|Head CT W and WO reduced contrast volume IV
46314-1|Internal auditory canal CT W and WO reduced contrast volume IV
46313-3|Pelvis CT W and WO reduced contrast volume IV
60515-4|Rectum and Colon CT 3D W air contrast PR
24586-0|Brain MRI W anesthesia
24936-7|Spine Cervical MRI W anesthesia
24977-1|Spine Lumbar MRI W anesthesia
25046-4|Unspecified body region CT W anesthesia
38022-0|Gallbladder US W cholecystokinin
25047-2|Unspecified body region CT W conscious sedation
25057-1|Unspecified body region MRI W conscious sedation
30599-5|Abdomen CT W contrast
24567-0|Abdomen retroperitoneum CT W contrast
38055-0|Unspecified body region US W contrast
36809-2|Hepatic artery CT angiogram W contrast IA
69162-6|Pulmonary artery - bilateral MRI angiogram W contrast IA
69238-4|Urinary Bladder and Urethra SPECT W contrast intra bladder during voiding
30853-6|Breast duct US W contrast intra duct
36941-3|Salivary gland CT W contrast intra salivary duct
37237-5|Sinus tract CT W contrast intra sinus tract
36115-4|Ankle MRI W contrast intraarticular
69102-2|Ankle - left CT W contrast intraarticular
36116-2|Ankle - left MRI W contrast intraarticular
69109-7|Ankle - right CT W contrast intraarticular
36117-0|Ankle - right MRI W contrast intraarticular
46319-0|Elbow MRI W contrast intraarticular
69103-0|Elbow - left CT W contrast intraarticular
36118-8|Elbow - left MRI W contrast intraarticular
69110-5|Elbow - right CT W contrast intraarticular
36119-6|Elbow - right MRI W contrast intraarticular
36120-4|Hip MRI W contrast intraarticular
69105-5|Hip - left CT W contrast intraarticular
36121-2|Hip - left MRI W contrast intraarticular
69112-1|Hip - right CT W contrast intraarticular
36122-0|Hip - right MRI W contrast intraarticular
36124-6|Knee CT W contrast intraarticular
36125-3|Knee MRI W contrast intraarticular
69106-3|Knee - left CT W contrast intraarticular
36126-1|Knee - left MRI W contrast intraarticular
69114-7|Knee - right CT W contrast intraarticular
36127-9|Knee - right MRI W contrast intraarticular
37238-3|Lower Extremity Joint CT W contrast intraarticular
69210-3|Lower Extremity Joint MRI W contrast intraarticular
36123-8|Sacroiliac Joint CT W contrast intraarticular
36128-7|Shoulder CT W contrast intraarticular
36129-5|Shoulder MRI W contrast intraarticular
38828-0|Shoulder - left CT W contrast intraarticular
36130-3|Shoulder - left MRI W contrast intraarticular
36131-1|Shoulder - right CT W contrast intraarticular
36132-9|Shoulder - right MRI W contrast intraarticular
36810-0|Upper Joint CT W contrast intraarticular
37444-7|Wrist MRI W contrast intraarticular
69107-1|Wrist - left CT W contrast intraarticular
37445-4|Wrist - left MRI W contrast intraarticular
69115-4|Wrist - right CT W contrast intraarticular
37446-2|Wrist - right MRI W contrast intraarticular
36811-8|Joint CT W contrast intraarticular
36812-6|Joint MRI W contrast intraarticular
37496-7|Spine Cervical CT W contrast intradisc
37509-7|Spine Lumbar CT W contrast intradisc
70931-1|Spine Thoracic CT W contrast intradisc
24734-6|Head Cistern CT W contrast IT
24934-2|Spine Cervical CT W contrast IT
48447-7|Spine Cervical MRI W contrast IT
24965-6|Spine Lumbar CT W contrast IT
48436-0|Spine Lumbar MRI W contrast IT
30596-1|Spine Thoracic CT W contrast IT
48439-4|Spine Thoracic MRI W contrast IT
36134-5|Abdomen MRI W contrast IV
36813-4|Abdomen and Pelvis CT W contrast IV
36828-2|Abdominal vessels CT angiogram W contrast IV
24533-2|Abdominal vessels MRI angiogram W contrast IV
69908-2|Abdominal vessels and Pelvis vessels CT angiogram W contrast IV
36943-9|Adrenal gland CT W contrast IV
44124-6|Adrenal gland MRI W contrast IV
36135-2|Ankle CT W contrast IV
36136-0|Ankle MRI W contrast IV
69163-4|Ankle - bilateral MRI W contrast IV
36137-8|Ankle - left CT W contrast IV
36138-6|Ankle - left MRI W contrast IV
36139-4|Ankle - right CT W contrast IV
36140-2|Ankle - right MRI W contrast IV
36142-8|Aorta CT W contrast IV
36141-0|Aorta CT angiogram W contrast IV
36143-6|Aorta abdominal CT W contrast IV
24545-6|Aorta thoracic CT W contrast IV
72255-3|Aorta and Femoral artery - bilateral CT angiogram W contrast IV
43503-2|Aorta and Lower extremity vessels CT angiogram W contrast IV
36144-4|Aortic arch CT angiogram W contrast IV
37499-1|Aortic stent CT angiogram W contrast IV
36145-1|Appendix CT W contrast IV
43504-0|Axilla - left MRI W contrast IV
43505-7|Axilla - right MRI W contrast IV
44125-3|Biliary ducts and Pancreatic duct MRI W contrast IV
69095-8|Bladder CT W contrast IV
24589-4|Brain MRI W contrast IV
48444-4|Brain.temporal MRI W contrast IV
37239-1|Brain and Internal auditory canal MRI W contrast IV
37215-1|Brain and Larynx MRI W contrast IV
42391-3|Brain and Pituitary and Sella turcica MRI W contrast IV
36149-3|Breast MRI W contrast IV
69190-7|Breast implant MRI W contrast IV
69167-5|Breast implant - bilateral MRI W contrast IV
36150-1|Breast - bilateral MRI W contrast IV
36151-9|Breast - left MRI W contrast IV
36152-7|Breast - right MRI W contrast IV
46323-2|Breast - unilateral MRI W contrast IV
36198-0|Calcaneus CT W contrast IV
36153-5|Calcaneus - left CT W contrast IV
36154-3|Calcaneus - right CT W contrast IV
36146-9|Carotid artery CT angiogram W contrast IV
36829-0|Carotid vessel MRI angiogram W contrast IV
24628-0|Chest CT W contrast IV
36156-8|Chest MRI W contrast IV
36266-5|Chest vessels CT angiogram W contrast IV
24659-5|Chest vessels MRI angiogram W contrast IV
42275-8|Chest and Abdomen CT W contrast IV
36942-1|Chest and Abdomen MRI W contrast IV
72254-6|Chest and Abdomen and Pelvis CT W contrast IV
37254-0|Circle of Willis MRI angiogram W contrast IV
42694-0|Clavicle MRI W contrast IV
48457-6|Clavicle - left MRI W contrast IV
48456-8|Clavicle - right MRI W contrast IV
36157-6|Elbow CT W contrast IV
36158-4|Elbow MRI W contrast IV
69170-9|Elbow - bilateral MRI W contrast IV
36159-2|Elbow - left CT W contrast IV
36160-0|Elbow - left MRI W contrast IV
36161-8|Elbow - right CT W contrast IV
36162-6|Elbow - right MRI W contrast IV
24691-8|Extremity CT W contrast IV
26184-2|Extremity - bilateral CT W contrast IV
26185-9|Extremity - left CT W contrast IV
26186-7|Extremity - right CT W contrast IV
36148-5|Face MRI W contrast IV
30801-5|Facial bones and Maxilla CT W contrast IV
24697-5|Facial bones and Sinuses CT W contrast IV
36172-5|Femur CT W contrast IV
69172-5|Femur - bilateral MRI W contrast IV
36174-1|Femur - left CT W contrast IV
36176-6|Femur - right CT W contrast IV
69195-6|Finger MRI W contrast IV
69205-3|Finger - left MRI W contrast IV
69215-2|Finger - right MRI W contrast IV
36178-2|Foot CT W contrast IV
36179-0|Foot MRI W contrast IV
36180-8|Foot - bilateral MRI W contrast IV
36181-6|Foot - left CT W contrast IV
36182-4|Foot - left MRI W contrast IV
36183-2|Foot - right CT W contrast IV
36184-0|Foot - right MRI W contrast IV
36185-7|Forearm CT W contrast IV
36186-5|Forearm MRI W contrast IV
69175-8|Forearm - bilateral MRI W contrast IV
36187-3|Forearm - left CT W contrast IV
36188-1|Forearm - left MRI W contrast IV
36189-9|Forearm - right CT W contrast IV
36190-7|Forearm - right MRI W contrast IV
36191-5|Hand CT W contrast IV
36192-3|Hand MRI W contrast IV
69178-2|Hand - bilateral MRI W contrast IV
36193-1|Hand - left CT W contrast IV
36194-9|Hand - left MRI W contrast IV
36195-6|Hand - right CT W contrast IV
36196-4|Hand - right MRI W contrast IV
24727-0|Head CT W contrast IV
36814-2|Head arteries CT angiogram W contrast IV
36826-6|Head veins MRI angiogram W contrast IV
36830-8|Head vessels CT angiogram W contrast IV
24593-6|Head vessels MRI angiogram W contrast IV
37498-3|Head vessels and Neck vessels CT angiogram W contrast IV
24747-8|Head Sagittal Sinus MRI angiogram W contrast IV
36197-2|Heart MRI W contrast IV
36200-4|Hip CT W contrast IV
36199-8|Hip MRI W contrast IV
36201-2|Hip - bilateral CT W contrast IV
36202-0|Hip - bilateral MRI W contrast IV
36203-8|Hip - left CT W contrast IV
36204-6|Hip - left MRI W contrast IV
36205-3|Hip - right CT W contrast IV
36206-1|Hip - right MRI W contrast IV
30583-9|Internal auditory canal CT W contrast IV
36155-0|Internal auditory canal MRI W contrast IV
46322-4|Kidney CT W contrast IV
36113-9|Kidney MRI W contrast IV
43766-5|Kidney - bilateral CT W contrast IV
36219-4|Kidney - bilateral MRI W contrast IV
24790-8|Kidney - bilateral X-ray tomograph W contrast IV
36220-2|Kidney - left MRI W contrast IV
36221-0|Kidney - right MRI W contrast IV
36222-8|Knee CT W contrast IV
36223-6|Knee MRI W contrast IV
69088-3|Knee - bilateral CT W contrast IV
36224-4|Knee - bilateral MRI W contrast IV
36225-1|Knee - left CT W contrast IV
36226-9|Knee - left MRI W contrast IV
36227-7|Knee - right CT W contrast IV
36228-5|Knee - right MRI W contrast IV
36229-3|Larynx CT W contrast IV
36230-1|Larynx MRI W contrast IV
24815-3|Liver CT W contrast IV
36231-9|Liver MRI W contrast IV
30624-1|Lower extremity CT W contrast IV
39293-6|Lower extremity MRI W contrast IV
36824-1|Lower extremity veins - left CT W contrast IV
36825-8|Lower extremity veins - right CT W contrast IV
36831-6|Lower extremity vessels CT angiogram W contrast IV
46324-0|Lower extremity vessels MRI angiogram W contrast IV
44135-2|Lower extremity vessels - bilateral MRI angiogram W contrast IV
50755-8|Lower extremity - bilateral CT W contrast IV
36163-4|Lower extremity - bilateral MRI W contrast IV
36213-7|Lower Extremity Joint MRI W contrast IV
36214-5|Lower extremity joint - left MRI W contrast IV
36215-2|Lower extremity joint - right MRI W contrast IV
36164-2|Lower extremity - left CT W contrast IV
36165-9|Lower extremity - left MRI W contrast IV
36166-7|Lower extremity - right CT W contrast IV
36167-5|Lower extremity - right MRI W contrast IV
36258-2|Lower leg CT W contrast IV
36259-0|Lower leg MRI W contrast IV
24820-3|Lower leg vessels MRI angiogram W contrast IV
43512-3|Lower leg vessels - bilateral MRI angiogram W contrast IV
42695-7|Lower leg - bilateral MRI W contrast IV
36260-8|Lower leg - left CT W contrast IV
36261-6|Lower leg - left MRI W contrast IV
36262-4|Lower leg - right CT W contrast IV
36263-2|Lower leg - right MRI W contrast IV
36232-7|Mandible CT W contrast IV
48446-9|Nasopharynx CT W contrast IV
36233-5|Nasopharynx MRI W contrast IV
24836-9|Nasopharynx and Neck CT W contrast IV
36235-0|Neck CT W contrast IV
24841-9|Neck MRI W contrast IV
36827-4|Neck veins MRI angiogram W contrast IV
36234-3|Neck vessels CT angiogram W contrast IV
24844-3|Neck vessels MRI angiogram W contrast IV
48449-3|Orbit CT W contrast IV
36820-9|Orbit MRI W contrast IV
36832-4|Orbit vessels MRI angiogram W contrast IV
24850-0|Orbit - bilateral CT W contrast IV
24852-6|Orbit - bilateral MRI W contrast IV
36821-7|Orbit - left MRI W contrast IV
36822-5|Orbit - right MRI W contrast IV
46320-8|Orbit and Face CT W contrast IV
39038-5|Orbit and Face MRI W contrast IV
46321-6|Orbit and Face and Neck MRI W contrast IV
36823-3|Ovary MRI W contrast IV
24858-3|Pancreas CT W contrast IV
36236-8|Pancreas MRI W contrast IV
37240-9|Parotid gland CT W contrast IV
37241-7|Parotid gland MRI W contrast IV
24866-6|Pelvis CT W contrast IV
36237-6|Pelvis MRI W contrast IV
42294-9|Pelvis vessels CT angiogram W contrast IV
24873-2|Pelvis vessels MRI angiogram W contrast IV
24878-1|Petrous bone CT W contrast IV
30590-4|Pituitary and Sella turcica CT W contrast IV
36238-4|Pituitary and Sella turcica MRI W contrast IV
36242-6|Posterior fossa CT W contrast IV
36243-4|Posterior fossa MRI W contrast IV
36244-2|Prostate MRI W contrast IV
36147-7|Pulmonary artery CT angiogram W contrast IV
36833-2|Renal vessels CT angiogram W contrast IV
30887-4|Renal vessels MRI angiogram W contrast IV
36217-8|Sacroiliac Joint CT W contrast IV
36218-6|Sacroiliac Joint MRI W contrast IV
36245-9|Sacrum CT W contrast IV
36246-7|Sacrum MRI W contrast IV
36247-5|Sacrum and Coccyx MRI W contrast IV
36248-3|Scapula - left MRI W contrast IV
36249-1|Scapula - right MRI W contrast IV
69221-0|Scrotum and Testicle MRI W contrast IV
36250-9|Shoulder CT W contrast IV
36251-7|Shoulder MRI W contrast IV
69184-0|Shoulder - bilateral MRI W contrast IV
36252-5|Shoulder - left CT W contrast IV
38830-6|Shoulder - left MRI W contrast IV
36253-3|Shoulder - right CT W contrast IV
36254-1|Shoulder - right MRI W contrast IV
36255-8|Sinuses CT W contrast IV
24915-1|Sinuses MRI W contrast IV
48440-2|Skull.base MRI W contrast IV
37253-2|Soft tissue MRI W contrast IV
37500-6|Spine vessels MRI angiogram W contrast IV
24933-4|Spine Cervical CT W contrast IV
24938-3|Spine Cervical MRI W contrast IV
37501-4|Cervical Spine vessels MRI angiogram W contrast IV
38061-8|Spine Cervical and Spine Thoracic and Spine Lumbar and Sacrum MRI W contrast IV
24964-9|Spine Lumbar CT W contrast IV
30678-7|Spine Lumbar MRI W contrast IV
37502-2|Lumbar Spine vessels MRI angiogram W contrast IV
24979-7|Spine Thoracic CT W contrast IV
24982-1|Spine Thoracic MRI W contrast IV
37503-0|Thoracic Spine vessels MRI angiogram W contrast IV
30622-5|Spleen CT W contrast IV
37242-5|Sternoclavicular Joint CT W contrast IV
36257-4|Sternum CT W contrast IV
36815-9|Temporal bone CT W contrast IV
38835-5|Temporal bone - left CT W contrast IV
36816-7|Temporal bone - right CT W contrast IV
37243-3|Temporomandibular joint CT W contrast IV
37244-1|Temporomandibular joint MRI W contrast IV
37245-8|Temporomandibular joint - bilateral MRI W contrast IV
37246-6|Temporomandibular joint - left CT W contrast IV
37247-4|Temporomandibular joint - left MRI W contrast IV
37248-2|Temporomandibular joint - right CT W contrast IV
37249-0|Temporomandibular joint - right MRI W contrast IV
36173-3|Thigh MRI W contrast IV
25003-5|Thigh vessels MRI angiogram W contrast IV
36175-8|Thigh - left MRI W contrast IV
36177-4|Thigh - right MRI W contrast IV
36239-2|Thoracic outlet MRI W contrast IV
24584-5|Thoracic outlet vessels MRI angiogram W contrast IV
26181-8|Thoracic outlet vessels - bilateral MRI angiogram W contrast IV
26182-6|Thoracic outlet vessels - left MRI angiogram W contrast IV
26183-4|Thoracic outlet vessels - right MRI angiogram W contrast IV
36240-0|Thoracic outlet - left MRI W contrast IV
36241-8|Thoracic outlet - right MRI W contrast IV
72243-9|Toes - left MRI W contrast IV
72240-5|Toes - right MRI W contrast IV
36207-9|Upper arm CT W contrast IV
36208-7|Upper arm MRI W contrast IV
69182-4|Upper arm - bilateral MRI W contrast IV
36209-5|Upper arm - left CT W contrast IV
36210-3|Upper arm - left MRI W contrast IV
36211-1|Upper arm - right CT W contrast IV
36212-9|Upper arm - right MRI W contrast IV
30626-6|Upper extremity CT W contrast IV
39037-7|Upper extremity MRI W contrast IV
42295-6|Upper extremity vessels CT angiogram W contrast IV
24549-8|Upper extremity vessels MRI angiogram W contrast IV
36168-3|Upper extremity - bilateral CT W contrast IV
69187-3|Upper extremity - bilateral MRI W contrast IV
36216-0|Upper extremity .joint MRI W contrast IV
36817-5|Upper extremity joint - bilateral MRI W contrast IV
36818-3|Upper extremity joint - left MRI W contrast IV
36819-1|Upper extremity joint - right MRI W contrast IV
36169-1|Upper extremity - left CT W contrast IV
38829-8|Upper extremity - left MRI W contrast IV
36170-9|Upper extremity - right CT W contrast IV
36171-7|Upper extremity - right MRI W contrast IV
36264-0|Uterus CT W contrast IV
36265-7|Uterus MRI W contrast IV
36834-0|Vessel CT angiogram W contrast IV
37447-0|Wrist CT W contrast IV
37448-8|Wrist MRI W contrast IV
69091-7|Wrist - bilateral CT W contrast IV
37449-6|Wrist - bilateral MRI W contrast IV
37450-4|Wrist - left CT W contrast IV
37451-2|Wrist - left MRI W contrast IV
37452-0|Wrist - right CT W contrast IV
37453-8|Wrist - right MRI W contrast IV
24753-6|Unspecified body region CT W contrast IV
49507-7|Unspecified body region MRI W contrast IV
25058-9|Unspecified body region MRI angiogram W contrast IV
72531-7|Rectum and Colon CT 3D W contrast IV and W air contrast PR
39450-2|Gastrointestine US W contrast PO
72246-2|Abdomen and Pelvis MRI W contrast PO and W and WO contrast IV
72250-4|Abdomen and Pelvis CT W contrast PO and W contrast IV
72247-0|Abdomen and Pelvis MRI W contrast PO and WO contrast IV
72245-4|Pelvis MRI W contrast PR at rest and maxmal sphincter contraction during straining and defecation
39648-1|Heart SPECT W dipyridamole and W radionuclide IV
44154-3|Heart SPECT W dipyridamole and W Tc-99m Sestamibi IV
42389-7|Pelvis MRI W endorectal coil
42388-9|Prostate MRI W endorectal coil
42270-9|Spine Cervical MRI W flexion and W extension
39682-0|SPECT W GA-67 IV
39638-2|Brain SPECT W I-123 IV
39755-4|Thyroid SPECT W I-131 IV
39839-6|SPECT W I-131 MIBG IV
39844-6|SPECT W In-111 Satumomab IV
41838-4|Prostate SPECT W In-111 Satumomab IV
41772-5|Bone SPECT W In-111 tagged WBC IV
46297-8|SPECT
39823-0|Bone marrow SPECT
24578-7|Bones SPECT
39632-5|Brain SPECT
39644-0|Breast SPECT
39770-3|Gastrointestine SPECT
39649-9|Heart SPECT
42310-3|Kidney SPECT
39852-9|Kidney - bilateral SPECT
39692-9|Liver SPECT
39876-8|Liver and Spleen SPECT
39628-3|Meckels diverticulum SPECT
39740-6|Parathyroid SPECT
43526-3|Unspecified body region SPECT
39938-6|Joint SPECT
46330-7|Abdomen CT W reduced contrast volume IV
46327-3|Chest CT W reduced contrast volume IV
46326-5|Facial bones and Maxilla CT W reduced contrast volume IV
46328-1|Head CT W reduced contrast volume IV
46325-7|Internal auditory canal CT W reduced contrast volume IV
46329-9|Pelvis CT W reduced contrast volume IV
42143-8|Uterus and Fallopian tubes US W saline intrauterine
58750-1|Heart MRI W stress
58749-3|Heart MRI W stress and W and WO contrast IV
39668-9|Heart SPECT W stress and W radionuclide IV
44152-7|Brain SPECT W Tc-99m bicisate IV
39743-0|Prostate SPECT W Tc-99m capromab pendatide IV
39640-8|Brain SPECT W Tc-99m DTPA IV
39641-6|Brain SPECT W Tc-99m glucoheptonate IV
44153-5|Kidney SPECT W Tc-99m glucoheptonate IV
39631-7|Brain SPECT W Tc-99m HMPAO IV
24817-9|Liver SPECT W Tc-99m IV
39851-1|Kidney - bilateral SPECT W Tc-99m Mertiatide IV
69229-3|Liver SPECT W Tc-99m SC IV
44151-9|Heart SPECT W Tc-99m Sestamibi IV
39691-1|Liver SPECT W Tc-99m tagged RBC IV
69234-3|Spleen SPECT W Tc-99m tagged RBC IV
39647-3|Heart SPECT W Tc-99m Tetrofosmin IV
39639-0|Brain SPECT W Tl-201 IV
42377-2|Brain CT W Xe-133 inhaled
46393-5|Liver CT W Xe-133 inhaled
42394-7|Pulmonary system CT W Xe-133 inhaled
36424-0|Abdomen CT WO contrast
30668-8|Abdomen MRI WO contrast
42291-5|Abdomen retroperitoneum CT WO contrast
36952-0|Abdomen and Pelvis CT WO contrast
36878-7|Abdominal vessels MRI angiogram WO contrast
36496-8|Acromioclavicular Joint MRI WO contrast
36953-8|Adrenal gland CT WO contrast
36954-6|Adrenal gland MRI WO contrast
36425-7|Ankle CT WO contrast
30680-3|Ankle MRI WO contrast
36879-5|Ankle vessels MRI angiogram WO contrast
69087-5|Ankle - bilateral CT WO contrast
69164-2|Ankle - bilateral MRI WO contrast
36426-5|Ankle - left CT WO contrast
36427-3|Ankle - left MRI WO contrast
36428-1|Ankle - right CT WO contrast
36429-9|Ankle - right MRI WO contrast
36430-7|Aorta CT WO contrast
44132-9|Aorta MRI angiogram WO contrast
36431-5|Aorta abdominal CT WO contrast
36432-3|Aorta abdominal MRI angiogram WO contrast
69119-6|Aorta thoracic CT angiogram WO contrast
36433-1|Aorta thoracic MRI angiogram WO contrast
44130-3|Aortic arch MRI angiogram WO contrast
36434-9|Appendix CT WO contrast
44123-8|Biliary ducts and Pancreatic duct MRI WO contrast
30657-1|Brain MRI WO contrast
48453-5|Brain.temporal MRI WO contrast
37278-9|Brain and Internal auditory canal MRI WO contrast
37279-7|Brain and Larynx MRI WO contrast
42393-9|Brain and Pituitary and Sella turcica MRI WO contrast
36436-4|Breast MRI WO contrast
69191-5|Breast implant MRI WO contrast
69168-3|Breast implant - bilateral MRI WO contrast
38064-2|Breast implant - left MRI WO contrast
38817-3|Breast implant - right MRI WO contrast
44119-6|Breast - bilateral CT WO contrast
36437-2|Breast - bilateral MRI WO contrast
36438-0|Breast - left MRI WO contrast
36439-8|Breast - right MRI WO contrast
46333-1|Breast - unilateral MRI WO contrast
36483-6|Calcaneus CT WO contrast
36440-6|Calcaneus - left CT WO contrast
36441-4|Calcaneus - right CT WO contrast
36880-3|Carotid vessel MRI angiogram WO contrast
29252-4|Chest CT WO contrast
36442-2|Chest MRI WO contrast
69084-2|Chest vessels CT angiogram WO contrast
36547-8|Chest vessels MRI angiogram WO contrast
42276-6|Chest and Abdomen CT WO contrast
72253-8|Chest and Abdomen and Pelvis CT WO contrast
42302-0|Clavicle MRI WO contrast
48459-2|Clavicle - left MRI WO contrast
48458-4|Clavicle - right MRI WO contrast
36443-0|Elbow CT WO contrast
30796-7|Elbow MRI WO contrast
36444-8|Elbow - bilateral CT WO contrast
69171-7|Elbow - bilateral MRI WO contrast
36445-5|Elbow - left CT WO contrast
36446-3|Elbow - left MRI WO contrast
36447-1|Elbow - right CT WO contrast
36448-9|Elbow - right MRI WO contrast
42278-2|Extremity CT WO contrast
69104-8|Extremity - left CT WO contrast
69111-3|Extremity - right CT WO contrast
36435-6|Face MRI WO contrast
30802-3|Facial bones and Maxilla CT WO contrast
72249-6|Facial bones and Sinuses CT WO contrast
36460-4|Femur CT WO contrast
69173-3|Femur - bilateral MRI WO contrast
36462-0|Femur - left CT WO contrast
36464-6|Femur - right CT WO contrast
69196-4|Finger MRI WO contrast
69206-1|Finger - left MRI WO contrast
69216-0|Finger - right MRI WO contrast
36466-1|Foot CT WO contrast
30681-1|Foot MRI WO contrast
36467-9|Foot - bilateral MRI WO contrast
36468-7|Foot - left CT WO contrast
36469-5|Foot - left MRI WO contrast
36470-3|Foot - right CT WO contrast
36471-1|Foot - right MRI WO contrast
36472-9|Forearm CT WO contrast
30683-7|Forearm MRI WO contrast
69176-6|Forearm - bilateral MRI WO contrast
36473-7|Forearm - left CT WO contrast
36474-5|Forearm - left MRI WO contrast
36475-2|Forearm - right CT WO contrast
36476-0|Forearm - right MRI WO contrast
36477-8|Hand CT WO contrast
30685-2|Hand MRI WO contrast
69179-0|Hand - bilateral MRI WO contrast
36478-6|Hand - left CT WO contrast
36479-4|Hand - left MRI WO contrast
36480-2|Hand - right CT WO contrast
36481-0|Hand - right MRI WO contrast
30799-1|Head CT WO contrast
36876-1|Head veins MRI angiogram WO contrast
42293-1|Head vessels CT angiogram WO contrast
36881-1|Head vessels MRI angiogram WO contrast
36482-8|Heart MRI WO contrast
36484-4|Hip CT WO contrast
30687-8|Hip MRI WO contrast
36485-1|Hip - bilateral CT WO contrast
36486-9|Hip - bilateral MRI WO contrast
36487-7|Hip - left CT WO contrast
36488-5|Hip - left MRI WO contrast
36489-3|Hip - right CT WO contrast
36490-1|Hip - right MRI WO contrast
30584-7|Internal auditory canal CT WO contrast
30658-9|Internal auditory canal MRI WO contrast
43770-7|Kidney CT WO contrast
43773-1|Kidney MRI WO contrast
36503-1|Kidney - bilateral CT WO contrast
36504-9|Kidney - bilateral MRI WO contrast
39359-5|Kidney - bilateral X-ray tomograph WO contrast
36505-6|Knee CT WO contrast
30691-0|Knee MRI WO contrast
69089-1|Knee - bilateral CT WO contrast
36506-4|Knee - bilateral MRI WO contrast
36507-2|Knee - left CT WO contrast
36508-0|Knee - left MRI WO contrast
36509-8|Knee - right CT WO contrast
36510-6|Knee - right MRI WO contrast
36511-4|Larynx CT WO contrast
48445-1|Larynx MRI WO contrast
30611-8|Liver CT WO contrast
30669-6|Liver MRI WO contrast
30625-8|Lower extremity CT WO contrast
39292-8|Lower extremity MRI WO contrast
44129-5|Lower extremity vessels MRI angiogram WO contrast
36450-5|Lower extremity vessels - bilateral MRI angiogram WO contrast
36882-9|Lower extremity vessels - left MRI angiogram WO contrast
38773-8|Lower extremity vessels - right MRI angiogram WO contrast
36449-7|Lower extremity - bilateral CT WO contrast
36451-3|Lower extremity - bilateral MRI WO contrast
36497-6|Lower Extremity Joint MRI WO contrast
36498-4|Lower extremity joint - left MRI WO contrast
36499-2|Lower extremity joint - right MRI WO contrast
36452-1|Lower extremity - left CT WO contrast
36453-9|Lower extremity - left MRI WO contrast
36454-7|Lower extremity - right CT WO contrast
36455-4|Lower extremity - right MRI WO contrast
36537-9|Lower leg CT WO contrast
30869-2|Lower leg MRI WO contrast
69185-7|Lower leg - bilateral MRI WO contrast
36538-7|Lower leg - left CT WO contrast
36539-5|Lower leg - left MRI WO contrast
36540-3|Lower leg - right CT WO contrast
36541-1|Lower leg - right MRI WO contrast
36512-2|Mandible CT WO contrast
36513-0|Nasopharynx MRI WO contrast
30585-4|Nasopharynx and Neck CT WO contrast
36514-8|Neck CT WO contrast
30660-5|Neck MRI WO contrast
36877-9|Neck veins MRI angiogram WO contrast
36549-4|Neck vessels MRI angiogram WO contrast
46331-5|Orbit CT WO contrast
36872-0|Orbit MRI WO contrast
30587-0|Orbit - bilateral CT WO contrast
30661-3|Orbit - bilateral MRI WO contrast
36873-8|Orbit - left MRI WO contrast
36874-6|Orbit - right MRI WO contrast
36956-1|Orbit and Face MRI WO contrast
46332-3|Orbit and Face and Neck MRI WO contrast
36875-3|Ovary MRI WO contrast
30613-4|Pancreas CT WO contrast
36515-5|Pancreas MRI WO contrast
37280-5|Parotid gland CT WO contrast
37281-3|Parotid gland MRI WO contrast
30615-9|Pelvis CT WO contrast
30673-8|Pelvis MRI WO contrast
36883-7|Pelvis vessels MRI angiogram WO contrast
30671-2|Pelvis and Hip MRI WO contrast
30589-6|Petrous bone CT WO contrast
30591-2|Pituitary and Sella turcica CT WO contrast
30666-2|Pituitary and Sella turcica MRI WO contrast
36543-7|Portal vein MRI angiogram WO contrast
36517-1|Posterior fossa CT WO contrast
36518-9|Posterior fossa MRI WO contrast
36519-7|Prostate MRI WO contrast
36544-5|Renal vein MRI angiogram WO contrast
44133-7|Renal vessels MRI angiogram WO contrast
36501-5|Sacroiliac Joint CT WO contrast
36502-3|Sacroiliac Joint MRI WO contrast
36520-5|Sacrum CT WO contrast
36521-3|Sacrum MRI WO contrast
36522-1|Sacrum and Coccyx MRI WO contrast
69118-8|Scapula CT WO contrast
36523-9|Scapula - left MRI WO contrast
38770-4|Scapula - right MRI WO contrast
36535-3|Scrotum and Testicle MRI WO contrast
36524-7|Shoulder CT WO contrast
30693-6|Shoulder MRI WO contrast
69090-9|Shoulder - bilateral CT WO contrast
36525-4|Shoulder - bilateral MRI WO contrast
36526-2|Shoulder - left CT WO contrast
38834-8|Shoulder - left MRI WO contrast
36527-0|Shoulder - right CT WO contrast
36528-8|Shoulder - right MRI WO contrast
36529-6|Sinuses CT WO contrast
30662-1|Sinuses MRI WO contrast
44112-1|Skull.base CT WO contrast
48687-8|Skull.base MRI WO contrast
37293-8|Soft tissue MRI WO contrast
37510-5|Spine vessels MRI angiogram WO contrast
30592-0|Spine Cervical CT WO contrast
30667-0|Spine Cervical MRI WO contrast
37511-3|Cervical Spine vessels MRI angiogram WO contrast
30854-4|Spine Cervical and Thoracic and Lumbar MRI WO contrast
30620-9|Spine Lumbar CT WO contrast
30679-5|Spine Lumbar MRI WO contrast
37994-1|Lumbar Spine vessels MRI angiogram WO contrast
37288-8|Spine Lumbosacral Junction CT WO contrast
30597-9|Spine Thoracic CT WO contrast
36532-0|Spine Thoracic MRI WO contrast
37512-1|Thoracic Spine vessels MRI angiogram WO contrast
30621-7|Spleen CT WO contrast
36533-8|Spleen MRI WO contrast
37282-1|Sternoclavicular Joint CT WO contrast
36534-6|Sternum CT WO contrast
44230-1|Superior mesenteric vessels MRI angiogram WO contrast
36866-2|Temporal bone CT WO contrast
36867-0|Temporal bone - left CT WO contrast
36868-8|Temporal bone - right CT WO contrast
37283-9|Temporomandibular joint CT WO contrast
37284-7|Temporomandibular joint MRI WO contrast
37285-4|Temporomandibular joint - bilateral MRI WO contrast
37286-2|Temporomandibular joint - left MRI WO contrast
37287-0|Temporomandibular joint - right MRI WO contrast
36461-2|Thigh MRI WO contrast
43514-9|Thigh vessels - left MRI angiogram WO contrast
43515-6|Thigh vessels - right MRI angiogram WO contrast
36463-8|Thigh - left MRI WO contrast
36465-3|Thigh - right MRI WO contrast
30654-8|Thoracic outlet MRI WO contrast
38833-0|Thoracic outlet - left MRI WO contrast
36516-3|Thoracic outlet - right MRI WO contrast
36955-3|Thyroid CT WO contrast
36536-1|Thyroid MRI WO contrast
72242-1|Toes - left MRI WO contrast
72239-7|Toes - right MRI WO contrast
36491-9|Upper arm CT WO contrast
30689-4|Upper arm MRI WO contrast
69183-2|Upper arm - bilateral MRI WO contrast
36492-7|Upper arm - left CT WO contrast
36493-5|Upper arm - left MRI WO contrast
36494-3|Upper arm - right CT WO contrast
36495-0|Upper arm - right MRI WO contrast
30627-4|Upper extremity CT WO contrast
39033-6|Upper extremity MRI WO contrast
36548-6|Upper extremity vessels MRI angiogram WO contrast
36456-2|Upper extremity - bilateral CT WO contrast
69188-1|Upper extremity - bilateral MRI WO contrast
36500-7|Upper extremity .joint MRI WO contrast
36869-6|Upper extremity joint - left MRI WO contrast
36870-4|Upper extremity joint - right MRI WO contrast
36457-0|Upper extremity - left CT WO contrast
38832-2|Upper extremity - left MRI WO contrast
36458-8|Upper extremity - right CT WO contrast
36459-6|Upper extremity - right MRI WO contrast
36542-9|Uterus MRI WO contrast
36545-2|Inferior vena cava MRI WO contrast
36546-0|Superior vena cava MRI WO contrast
37459-5|Wrist CT WO contrast
37460-3|Wrist MRI WO contrast
43516-4|Wrist vessels - left MRI angiogram WO contrast
43517-2|Wrist vessels - right MRI angiogram WO contrast
37461-1|Wrist - bilateral CT WO contrast
37462-9|Wrist - bilateral MRI WO contrast
37463-7|Wrist - left CT WO contrast
37464-5|Wrist - left MRI WO contrast
37465-2|Wrist - right CT WO contrast
37466-0|Wrist - right MRI WO contrast
43525-5|Unspecified body region CT WO contrast
69223-6|Unspecified body region MRI WO contrast
36871-2|Joint MRI WO contrast
24787-4|Kidney - bilateral X-ray tomograph WO contrast and 10M post contrast IV
30712-4|Hip US WO developmental joint assessment
25051-4|Unspecified body region CT Multisectional sagittal
25060-5|Unspecified body region US No charge
24620-7|Catheter Fluoroscopy Patency check W contrast via catheter
24882-3|Popliteal artery Fluoroscopic angiogram Percutaneous transluminal angioplasty of vessel W contrast IA
69252-5|Pulmonary artery Fluoroscopic angiogram Percutaneous transluminal angioplasty of vessel W contrast IA
69248-3|Renal artery Fluoroscopic angiogram Percutaneous transluminal angioplasty of vessel W contrast IA
69301-0|Upper extremity vein Fluoroscopic angiogram Percutaneous transluminal angioplasty of vessel W contrast IV
24875-7|Peripheral vessel US.doppler Peripheral plane
24998-7|Placement check of gastrostomy tube W contrast via GI tube
44226-9|Colon Fluoroscopy Reduction W views W barium contrast PR
30636-5|Colon Fluoroscopy Reduction W views W contrast PR
25073-8|Vessel Fluoroscopic angiogram Removal of foreign body from vascular space
25015-9|Upper GI tract Replacement of percutaneous gastrojejunostomy
29757-2|Colposcopy study
18746-8|Colonoscopy study
18753-4|Flexible sigmoidoscopy study
11525-3|Obstetrical ultrasound study
18744-3|Bronchoscopy study
38269-7|Study report Skeletal system DXA
17787-3|Thyroid Scan Study report
18751-8|Endoscopy study
18748-4|Diagnostic imaging study
24783-3|Kidney - bilateral Fluoroscopy Urodynamics
25065-4|Unspecified body region Fluoroscopy 15 minutes
25068-8|Unspecified body region Fluoroscopy 1 hour
43471-2|Unspecified body region Fluoroscopy 2 hour
25066-2|Unspecified body region Fluoroscopy 30 minutes
25067-0|Unspecified body region Fluoroscopy 45 minutes
43472-0|Unspecified body region Fluoroscopy 90 minutes
42702-1|Unspecified body region Fluoroscopy Greater than 1 hour
42703-9|Unspecified body region Fluoroscopy Less than 1 hour
36550-2|Abdomen X-ray Single view
36551-0|Ankle X-ray Single view
69307-7|Ankle - left X-ray Single view
69314-3|Ankle - right X-ray Single view
46335-6|Breast - bilateral Mammogram Single view
46336-4|Breast - left Mammogram Single view
46337-2|Breast - right Mammogram Single view
46338-0|Breast - unilateral Mammogram Single view
36564-3|Calcaneus X-ray Single view
69311-9|Calcaneus - left X-ray Single view
69319-2|Calcaneus - right X-ray Single view
36554-4|Chest X-ray Single view
42699-9|Chest and Abdomen X-ray Single view
36555-1|Clavicle X-ray Single view
36556-9|Elbow X-ray Single view
69308-5|Elbow - left X-ray Single view
69315-0|Elbow - right X-ray Single view
42153-7|Extremity X-ray Single view
36559-3|Femur X-ray Single view
36560-1|Femur - left X-ray Single view
37689-7|Femur - right X-ray Single view
36561-9|Foot X-ray Single view
69309-3|Foot - left X-ray Single view
69316-8|Foot - right X-ray Single view
36563-5|Hand X-ray Single view
69310-1|Hand - left X-ray Single view
69318-4|Hand - right X-ray Single view
24761-9|Hip X-ray Single view
26400-2|Hip - bilateral X-ray Single view
26401-0|Hip - left X-ray Single view
26402-8|Hip - right X-ray Single view
36565-0|Humerus X-ray Single view
69312-7|Humerus - left X-ray Single view
69320-0|Humerus - right X-ray Single view
36566-8|Knee - bilateral X-ray Single view
36567-6|Knee - left X-ray Single view
37741-6|Knee - right X-ray Single view
36557-7|Lower extremity - bilateral X-ray Single view
36558-5|Lower extremity - left X-ray Single view
37764-8|Lower extremity - right X-ray Single view
37614-5|Patella X-ray Single view
69152-7|Patella - left X-ray Single view
69260-8|Patella - right X-ray Single view
37616-0|Pelvis X-ray Single view
69317-6|Radius - right and Ulna - right X-ray Single view
42313-7|Ribs - left X-ray Single view
42314-5|Ribs - right X-ray Single view
37654-1|Scapula X-ray Single view
30748-8|Shoulder X-ray Single view
36568-4|Shoulder - bilateral X-ray Single view
36569-2|Shoulder - left X-ray Single view
37792-9|Shoulder - right X-ray Single view
37851-3|Sinuses X-ray Single view
24917-7|Skull X-ray Single view
48695-1|Skull.base X-ray Single view
24940-9|Spine Cervical X-ray Single view
30773-6|Spine Lumbar X-ray Single view
37904-0|Spine Thoracic X-ray Single view
38121-0|Spine Thoracic and Lumbar X-ray Single view
69313-5|Tibia - left and Fibula - left X-ray Single view
69321-8|Tibia - right and Fibula - right X-ray Single view
37894-3|Tibia and Fibula X-ray Single view
37924-8|Wrist X-ray Single view
42419-2|Wrist - bilateral X-ray Single view
36570-0|Wrist - left X-ray Single view
37825-7|Wrist - right X-ray Single view
30642-3|Unspecified body region Fluoroscopy Single view
30787-6|Joint X-ray Single view
44176-6|Hip X-ray Single view portable
41775-8|Pelvis X-ray Single view portable
30749-6|Shoulder X-ray Single view portable
30722-3|Skull X-ray Single view portable
30724-9|Spine Cervical X-ray Single view portable
30774-4|Spine Lumbar X-ray Single view portable
70932-9|Spine Thoracic X-ray Single view portable
25063-9|Vessel Fluoroscopic angiogram Single view W contrast IA
69268-1|Breast duct Mammogram Single view W contrast intra duct
49510-1|Breast duct - left Mammogram Single view W contrast intra duct
49509-3|Breast duct - right Mammogram Single view W contrast intra duct
24715-5|Gastrointestine upper Fluoroscopy Single view W contrast PO
37513-9|Tibia - bilateral X-ray 10 degree caudal angle
37514-7|Tibia - left X-ray 10 degree caudal angle
38806-6|Tibia - right X-ray 10 degree caudal angle
37467-8|Acromioclavicular Joint X-ray 10 degree cephalic angle
37468-6|Shoulder - bilateral X-ray 30 degree caudal angle
42431-7|Knee - right X-ray 30 degree standing
69079-2|Clavicle X-ray 45 degree cephalic angle
37469-4|Clavicle - bilateral X-ray 45 degree cephalic angle
37470-2|Clavicle - left X-ray 45 degree cephalic angle
38803-3|Clavicle - right X-ray 45 degree cephalic angle
24799-9|Abdomen X-ray AP single view
36583-3|Acromioclavicular joint - left X-ray AP single view
37662-4|Acromioclavicular joint - right X-ray AP single view
36571-8|Ankle X-ray AP single view
36572-6|Chest X-ray AP single view
36573-4|Clavicle X-ray AP single view
36575-9|Femur X-ray AP single view
36576-7|Finger fifth X-ray AP single view
36577-5|Finger fourth X-ray AP single view
36578-3|Finger third X-ray AP single view
36579-1|Foot X-ray AP single view
36580-9|Foot - bilateral X-ray AP single view
36581-7|Hip X-ray AP single view
36582-5|Hip - left X-ray AP single view
37726-7|Hip - right X-ray AP single view
36584-1|Knee X-ray AP single view
36585-8|Knee - bilateral X-ray AP single view
48462-6|Knee - left X-ray AP single view
48463-4|Knee - right X-ray AP single view
36574-2|Lower extremity X-ray AP single view
42439-0|Neck X-ray AP single view
37622-8|Pelvis X-ray AP single view
39050-0|Ribs X-ray AP single view
36958-7|Ribs - bilateral X-ray AP single view
36959-5|Ribs - left X-ray AP single view
37783-8|Ribs - right X-ray AP single view
39048-4|Scapula X-ray AP single view
37842-2|Shoulder X-ray AP single view
36586-6|Shoulder - bilateral X-ray AP single view
36587-4|Shoulder - left X-ray AP single view
37798-6|Shoulder - right X-ray AP single view
69269-9|Skull X-ray AP single view
30725-6|Spine Cervical X-ray AP single view
24948-2|Spine Cervical Odontoid and Cervical axis X-ray AP single view
30777-7|Spine Lumbar X-ray AP single view
30752-0|Spine Thoracic X-ray AP single view
39049-2|Spine Thoracic and Lumbar X-ray AP single view
37880-2|Sternoclavicular Joint X-ray AP single view
37890-1|Thumb X-ray AP single view
37897-6|Tibia and Fibula X-ray AP single view
39402-3|Shoulder X-ray AP (W internal rotation and W external rotation)
37634-3|Pelvis X-ray AP 20 degree cephalic angle
30734-8|Chest X-ray AP lateral-decubitus
30735-5|Chest X-ray AP lateral-decubitus portable
24561-3|Abdomen X-ray AP left lateral-decubitus
24637-1|Chest X-ray AP left lateral-decubitus
24560-5|Abdomen X-ray AP left lateral-decubitus portable
24636-3|Chest X-ray AP left lateral-decubitus portable
36588-2|Abdomen X-ray AP portable single view
36589-0|Chest X-ray AP portable single view
30727-2|Spine Cervical X-ray AP portable single view
30729-8|Spine Cervical Odontoid and Cervical axis X-ray AP portable single view
30755-3|Spine Thoracic X-ray AP portable single view
24563-9|Abdomen X-ray AP right lateral-decubitus
43466-2|Chest X-ray AP right lateral-decubitus
24652-0|Chest X-ray AP right lateral-decubitus portable
43778-0|Chest X-ray AP supine portable
24564-7|Abdomen X-ray AP upright portable
36960-3|Chest X-ray AP upright portable
24807-0|Knee X-ray AP single view standing
26358-2|Knee - bilateral X-ray AP single view standing
26359-0|Knee - left X-ray AP single view standing
26360-8|Knee - right X-ray AP single view standing
44177-4|Lower extremity - bilateral X-ray AP single view standing
38849-6|Lower extremity - left X-ray AP single view standing
37733-3|Lower extremity - right X-ray AP single view standing
42420-0|Pelvis X-ray AP single view standing
42378-0|Spine Lumbar X-ray AP single view W left bending
39410-6|Spine Thoracic X-ray AP single view W left bending
42379-8|Spine Lumbar X-ray AP single view W right bending
39411-4|Spine Thoracic X-ray AP single view W right bending
24723-9|Hand X-ray arthritis
26355-8|Hand - bilateral X-ray arthritis
26356-6|Hand - left X-ray arthritis
26357-4|Hand - right X-ray arthritis
42395-4|Foot sesamoid bones - bilateral X-ray axial
42396-2|Foot sesamoid bones - left X-ray axial
36962-9|Breast Mammogram axillary
37849-7|Shoulder X-ray axillary
36963-7|Shoulder - bilateral X-ray axillary
36964-5|Shoulder - left X-ray axillary
37800-0|Shoulder - right X-ray axillary
36965-2|Hand X-ray Ball Catcher
37471-0|Hand - bilateral X-ray Bora
37472-8|Hand - left X-ray Bora
38804-1|Hand - right X-ray Bora
36966-0|Hand - bilateral X-ray Brewerton
36967-8|Hand - left X-ray Brewerton
38775-3|Hand - right X-ray Brewerton
37928-9|Wrist X-ray Brewerton
37857-0|Sinuses X-ray Caldwell
69132-9|Hip X-ray Danelius Miller
69141-0|Hip - left X-ray Danelius Miller
39514-5|Hip - right X-ray Danelius Miller
37625-1|Pelvis X-ray Ferguson
37650-9|Sacroiliac Joint X-ray Ferguson
65799-9|Kidney - bilateral Fluoroscopy View for cyst examination
65800-5|Kidney - left Fluoroscopy View for cyst examination
65801-3|Kidney - right Fluoroscopy View for cyst examination
37297-9|Abdomen and Fetus X-ray View for fetal age
39149-0|Gastrointestinal system and Respiratory system X-ray for foreign body
36973-6|Hip X-ray Friedman
37843-0|Shoulder X-ray Garth
36974-4|Shoulder - left X-ray Garth
37801-8|Shoulder - right X-ray Garth
37844-8|Shoulder X-ray Grashey
37035-3|Shoulder - bilateral X-ray Grashey
37473-6|Shoulder - left X-ray Grashey
38805-8|Shoulder - right X-ray Grashey
36975-1|Calcaneus - bilateral X-ray Harris
36977-7|Calcaneus - left X-ray Harris
38776-1|Calcaneus - right X-ray Harris
36976-9|Foot X-ray Harris
36978-5|Knee X-ray Holmblad
37628-5|Pelvis X-ray inlet
36979-3|Elbow X-ray Jones
36980-1|Elbow - left X-ray Jones
38777-9|Elbow - right X-ray Jones
36981-9|Hip X-ray Judet
36982-7|Hip - bilateral X-ray Judet
36983-5|Hip - left X-ray Judet
37732-5|Hip - right X-ray Judet
36620-3|Chest X-ray left anterior oblique
36591-6|Abdomen X-ray lateral
36592-4|Ankle X-ray lateral
39051-8|Chest X-ray lateral
36593-2|Femur X-ray lateral
36594-0|Finger fifth X-ray lateral
36595-7|Finger fourth X-ray lateral
36596-5|Finger second X-ray lateral
36597-3|Finger third X-ray lateral
36598-1|Foot - left X-ray lateral
37703-6|Foot - right X-ray lateral
36599-9|Hand X-ray lateral
36600-5|Hand - bilateral X-ray lateral
36601-3|Hand - left X-ray lateral
37712-7|Hand - right X-ray lateral
36602-1|Hip X-ray lateral
36603-9|Hip - left X-ray lateral
37730-9|Hip - right X-ray lateral
36604-7|Knee X-ray lateral
36605-4|Knee - bilateral X-ray lateral
36606-2|Knee - left X-ray lateral
37751-5|Knee - right X-ray lateral
24843-5|Neck X-ray lateral
37629-3|Pelvis X-ray lateral
39053-4|Ribs X-ray lateral
38857-9|Ribs - left X-ray lateral
37784-6|Ribs - right X-ray lateral
37858-8|Sinuses X-ray lateral
24920-1|Skull X-ray lateral
24943-3|Spine Cervical X-ray lateral
24969-8|Spine Lumbar X-ray lateral
30756-1|Spine Thoracic X-ray lateral
37891-9|Thumb X-ray lateral
37893-5|Tibia and Fibula X-ray lateral
37930-5|Wrist X-ray lateral
36984-3|Abdomen X-ray lateral crosstable
36985-0|Hip X-ray lateral crosstable
36986-8|Hip - bilateral X-ray lateral crosstable
36987-6|Hip - left X-ray lateral crosstable
37727-5|Hip - right X-ray lateral crosstable
36988-4|Knee X-ray lateral crosstable
37872-9|Skull X-ray lateral crosstable
36989-2|Spine Cervical X-ray lateral crosstable
36990-0|Spine Lumbar X-ray lateral crosstable
37903-2|Spine Thoracic X-ray lateral crosstable
36991-8|Spine Cervical X-ray lateral crosstable portable
36992-6|Spine Lumbar X-ray lateral crosstable portable
30786-8|Hip X-ray lateral frog
36993-4|Hip - bilateral X-ray lateral frog
36994-2|Hip - left X-ray lateral frog
37729-1|Hip - right X-ray lateral frog
37626-9|Pelvis X-ray lateral frog
36999-1|Knee - bilateral X-ray lateral hyperextension
37000-7|Knee - left X-ray lateral hyperextension
37750-7|Knee - right X-ray lateral hyperextension
37909-9|Spine Thoracic X-ray lateral hyperextension
41774-1|Neck X-ray lateral portable
30757-9|Spine Thoracic X-ray lateral portable
37515-4|Spine Lumbosacral Junction X-ray lateral spot
37516-2|Spine Lumbosacral Junction X-ray lateral spot standing
38066-7|Hip - left X-ray lateral during surgery
38819-9|Hip - right X-ray lateral during surgery
37001-5|Foot X-ray lateral standing
37002-3|Knee - left X-ray lateral standing
37754-9|Knee - right X-ray lateral standing
37003-1|Spine Lumbar X-ray lateral standing
37910-7|Spine Thoracic X-ray lateral standing
36997-5|Spine Cervical X-ray lateral W extension
36971-0|Wrist - left X-ray lateral W extension
37833-1|Wrist - right X-ray lateral W extension
36998-3|Spine Cervical X-ray lateral W flexion
36972-8|Wrist - left X-ray lateral W flexion
37834-9|Wrist - right X-ray lateral W flexion
37004-9|Knee X-ray Laurin
36995-9|Abdomen X-ray left lateral
30737-1|Chest X-ray left lateral
30738-9|Chest X-ray left lateral portable
24639-7|Chest X-ray left lateral upright
24638-9|Chest X-ray left lateral upright portable
37008-0|Chest X-ray left oblique
37009-8|Spine Lumbar X-ray left oblique
24641-3|Chest X-ray left oblique portable
24640-5|Chest X-ray lordotic
38069-1|Abdomen X-ray left posterior oblique
37005-6|Breast - left Mammogram magnification
37773-9|Breast - right Mammogram magnification
42441-6|Neck X-ray magnification
24801-3|Knee X-ray Merchants
26283-2|Knee - bilateral X-ray Merchants
26284-0|Knee - left X-ray Merchants
26285-7|Knee - right X-ray Merchants
37006-4|Breast - bilateral Mammogram MLO
37007-2|Ankle X-ray Mortise
37475-1|Ankle - left X-ray Mortise W manual stress
37671-5|Ankle - right X-ray Mortise W manual stress
38067-5|Breast - bilateral Mammogram nipple profile
36607-0|Abdomen X-ray oblique single view
36609-6|Femur X-ray oblique single view
36610-4|Finger fifth X-ray oblique single view
36611-2|Finger fourth X-ray oblique single view
36612-0|Finger second X-ray oblique single view
36613-8|Finger third X-ray oblique single view
36614-6|Foot X-ray oblique single view
36615-3|Foot - left X-ray oblique single view
37704-4|Foot - right X-ray oblique single view
36616-1|Hand X-ray oblique single view
36617-9|Hip X-ray oblique single view
36618-7|Hip - bilateral X-ray oblique single view
30778-5|Spine Lumbar X-ray oblique single view
30758-7|Spine Thoracic X-ray oblique single view
37892-7|Thumb X-ray oblique single view
44178-2|Spine Lumbar X-ray oblique view and (views W right bending and W left bending)
37545-1|Hip - left X-ray oblique crosstable
37728-3|Hip - right X-ray oblique crosstable
30759-5|Spine Thoracic X-ray oblique portable
37631-9|Pelvis X-ray outlet
37845-5|Shoulder X-ray outlet
37012-2|Shoulder - bilateral X-ray outlet
37013-0|Shoulder - left X-ray outlet
37802-6|Shoulder - right X-ray outlet
36621-1|Hand X-ray PA
36622-9|Hand - bilateral X-ray PA
36623-7|Hand - left X-ray PA
37714-3|Hand - right X-ray PA
69270-7|Skull X-ray PA
37931-3|Wrist X-ray PA
36624-5|Wrist - bilateral X-ray PA
37015-5|Abdomen X-ray PA prone
24648-8|Chest X-ray PA upright
37014-8|Knee - left X-ray PA standing
37755-6|Knee - right X-ray PA standing
37477-7|Knee X-ray PA standing and W 45 degree flexion
37476-9|Knee X-ray PA W 45 degree flexion
39324-9|Wrist - left X-ray PA W clenched fist
69263-2|Wrist - right X-ray PA W clenched fist
24828-6|Mandible X-ray panorex
24871-6|Pelvis X-ray pelvimetry
37998-2|Elbow X-ray radial head capitellar
37999-0|Elbow - bilateral X-ray radial head capitellar
38000-6|Elbow - left X-ray radial head capitellar
38006-3|Elbow - right X-ray radial head capitellar
38068-3|Chest X-ray right anterior oblique
36996-7|Abdomen X-ray right lateral
37010-6|Chest X-ray right oblique
37011-4|Spine Lumbar X-ray right oblique
37018-9|Knee X-ray Rosenberg standing
37020-5|Knee - bilateral X-ray Rosenberg standing
37019-7|Knee - left X-ray Rosenberg standing
37752-3|Knee - right X-ray Rosenberg standing
39323-1|Abdomen X-ray right posterior oblique
49511-9|Femoral artery Fluoroscopic angiogram runoff W and WO contrast IA
24699-1|Femoral artery Fluoroscopic angiogram runoff W contrast IA
26178-4|Femoral artery - bilateral Fluoroscopic angiogram runoff W contrast IA
26179-2|Femoral artery - left Fluoroscopic angiogram runoff W contrast IA
26180-0|Femoral artery - right Fluoroscopic angiogram runoff W contrast IA
42812-8|Wrist X-ray scaphoid single view
42813-6|Wrist - bilateral X-ray scaphoid single view
42814-4|Wrist - left X-ray scaphoid single view
42811-0|Wrist - right X-ray scaphoid single view
44206-1|Spine Thoracic and Lumbar X-ray scoliosis single view
30714-0|Spine Thoracic and Lumbar X-ray scoliosis AP
42426-7|Spine Thoracic and Lumbar X-ray scoliosis AP sitting
37659-0|Spine Thoracic and Lumbar X-ray scoliosis AP standing
42428-3|Spine Thoracic and Lumbar X-ray scoliosis AP standing and in brace
42429-1|Spine Thoracic and Lumbar X-ray scoliosis AP standing and W right bending
42427-5|Spine Thoracic and Lumbar X-ray scoliosis lateral sitting
37660-8|Spine Thoracic and Lumbar X-ray scoliosis lateral standing
37846-3|Sternoclavicular Joint X-ray Serendipity
37298-7|Sternoclavicular joint - bilateral X-ray Serendipity
37299-5|Sternoclavicular joint - left X-ray Serendipity
37808-3|Sternoclavicular joint - right X-ray Serendipity
43671-7|Thyroid Scan spot
42471-3|Pelvis X-ray stereo
42474-7|Skull X-ray stereo
39516-0|Shoulder X-ray Stryker Notch
37024-7|Shoulder - bilateral X-ray Stryker Notch
37025-4|Shoulder - left X-ray Stryker Notch
37791-1|Shoulder - right X-ray Stryker Notch
39517-8|Shoulder X-ray Stryker Notch and West Point
37861-2|Sinuses X-ray submentovertex
37026-2|Skull X-ray submentovertex
43780-6|Knee X-ray Sunrise
37027-0|Knee - bilateral X-ray Sunrise
43779-8|Knee - left X-ray Sunrise
69256-6|Knee - right X-ray Sunrise
69239-2|Patella X-ray Sunrise
69069-3|Patella - bilateral X-ray Sunrise
69064-4|Knee - bilateral X-ray Sunrise and (views standing)
69149-3|Knee - left X-ray Sunrise and (views standing)
42432-5|Knee - right X-ray Sunrise and (views standing)
24944-1|Spine Cervical X-ray Swimmers
37028-8|Breast Mammogram tangential
37029-6|Breast - bilateral Mammogram tangential
37030-4|Breast - left Mammogram tangential
37770-5|Breast - right Mammogram tangential
37870-3|Skull X-ray Towne
24668-6|Colon Fluoroscopy transit Post solid contrast
37031-2|Humerus X-ray transthoracic
37032-0|Humerus - bilateral X-ray transthoracic
37033-8|Humerus - left X-ray transthoracic
38007-1|Humerus - right X-ray transthoracic
37034-6|Shoulder - left X-ray transthoracic
38779-5|Shoulder - right X-ray transthoracic
37300-1|Spine Lumbosacral Junction X-ray true AP
37037-9|Breast Mammogram true lateral
37038-7|Breast - bilateral Mammogram true lateral
38855-3|Breast - left Mammogram true lateral
37771-3|Breast - right Mammogram true lateral
37039-5|Hip X-ray true lateral
37040-3|Hip - left X-ray true lateral
38772-0|Hip - right X-ray true lateral
30790-0|Knee X-ray tunnel
37041-1|Knee - bilateral X-ray tunnel
37042-9|Knee - left X-ray tunnel
37761-4|Knee - right X-ray tunnel
38842-1|Wrist - left X-ray tunnel.carpal
37677-2|Wrist - right X-ray tunnel.carpal
37043-7|Knee - left X-ray tunnel standing
37756-4|Knee - right X-ray tunnel standing
37044-5|Wrist - left X-ray ulnar deviation
37645-9|Wrist - right X-ray ulnar deviation
37045-2|Wrist - bilateral X-ray ulnar variance
37046-0|Abdomen X-ray upright
37047-8|Shoulder - bilateral X-ray Velpeau axillary
37048-6|Shoulder - left X-ray Velpeau axillary
38780-3|Shoulder - right X-ray Velpeau axillary
37049-4|Hip X-ray Von rossen
37613-7|Orbit - bilateral X-ray Waters
37863-8|Sinuses X-ray Waters
24921-9|Skull X-ray Waters
42473-9|Sinuses X-ray Waters stereo
38117-8|Sinuses X-ray Waters upright
30751-2|Shoulder X-ray West Point
37050-2|Shoulder - bilateral X-ray West Point
37051-0|Shoulder - left X-ray West Point
37809-1|Shoulder - right X-ray West Point
42680-9|Breast Mammogram XCCL
37052-8|Breast - bilateral Mammogram XCCL
37053-6|Breast - left Mammogram XCCL
37772-1|Breast - right Mammogram XCCL
37656-6|Scapula X-ray Y
37055-1|Scapula - bilateral X-ray Y
37054-4|Scapula - left X-ray Y
37790-3|Scapula - right X-ray Y
37847-1|Shoulder X-ray Y
38858-7|Shoulder - left X-ray Y
37805-9|Shoulder - right X-ray Y
37848-9|Acromioclavicular Joint X-ray Zanca
37056-9|Acromioclavicular joint - bilateral X-ray Zanca
37057-7|Acromioclavicular joint - left X-ray Zanca
37810-9|Acromioclavicular joint - right X-ray Zanca
41793-1|Abdomen X-ray during surgery
41790-7|Chest X-ray during surgery
24656-1|Chest Fluoroscopy during surgery
39047-6|Hip Fluoroscopy during surgery
38065-9|Hip - left X-ray during surgery
38818-1|Hip - right X-ray during surgery
42008-3|Humerus X-ray during surgery
24893-0|Rectum Fluoroscopy post contrast PR during defecation
37058-5|Calcaneus - bilateral X-ray standing
37059-3|Hip - bilateral X-ray standing
37207-8|Hip - left X-ray standing
37731-7|Hip - right X-ray standing
44205-3|Lower extremity - bilateral X-ray standing
38850-4|Lower extremity - left X-ray standing
37734-1|Lower extremity - right X-ray standing
37633-5|Pelvis X-ray standing
39144-1|Gastrointestine upper Fluoroscopy W air contrast PO
69302-8|Wrist X-ray W clenched fist
36968-6|Wrist - bilateral X-ray W clenched fist
30639-9|Vessel Fluoroscopic angiogram W contrast
42470-5|Gastrointestine upper and Gallbladder Fluoroscopy W contrast PO
30809-8|Upper Gastrointestine and Small bowel Fluoroscopy W contrast PO
42469-7|Gastrointestine upper and Small bowel and Gallbladder Fluoroscopy W contrast PO
38001-4|Chest X-ray W expiration
38002-2|Chest X-ray W inspiration
37060-1|Fetal X-ray
37636-8|Abdomen X-ray
46341-4|Abdomen Fluoroscopy
24535-7|Acetabulum X-ray
26133-9|Acetabulum - bilateral X-ray
26134-7|Acetabulum - left X-ray
26135-4|Acetabulum - right X-ray
24536-5|Acromioclavicular Joint X-ray
26136-2|Acromioclavicular joint - bilateral X-ray
26137-0|Acromioclavicular joint - left X-ray
26138-8|Acromioclavicular joint - right X-ray
24541-5|Ankle X-ray
26097-6|Ankle - bilateral X-ray
26098-4|Ankle - left X-ray
51395-2|Ankle - left and Foot.left X-ray
26099-2|Ankle - right X-ray
51394-5|Ankle - right and Foot - right X-ray
36625-2|Breast Mammogram
46342-2|Breast FFD mammogram
38070-9|Breast implant Mammogram
38071-7|Breast implant - bilateral Mammogram
38072-5|Breast implant - left Mammogram
38820-7|Breast implant - right Mammogram
46380-2|Breast Implant - unilateral Mammogram
24597-7|Breast specimen Mammogram
38079-0|Breast specimen - bilateral Mammogram
38080-8|Breast specimen - left Mammogram
38821-5|Breast specimen - right Mammogram
36626-0|Breast - bilateral Mammogram
36627-8|Breast - left Mammogram
37774-7|Breast - right Mammogram
46339-8|Breast - unilateral Mammogram
24612-4|Calcaneus X-ray
26100-8|Calcaneus - bilateral X-ray
26101-6|Calcaneus - left X-ray
26102-4|Calcaneus - right X-ray
30745-4|Chest X-ray
30631-6|Chest Fluoroscopy
42269-1|Chest and Abdomen X-ray
24664-5|Clavicle X-ray
26106-5|Clavicle - bilateral X-ray
26107-3|Clavicle - left X-ray
26108-1|Clavicle - right X-ray
30883-3|Coccyx X-ray
24676-9|Elbow X-ray
26109-9|Elbow - bilateral X-ray
26110-7|Elbow - left X-ray
26111-5|Elbow - right X-ray
46381-0|Elbow+Radius+Ulna X-ray
37637-6|Extremity X-ray
24695-9|Facial bones X-ray
37303-5|Facial bones and Zygomatic arch X-ray
24704-9|Femur X-ray
26118-0|Femur - bilateral X-ray
26120-6|Femur - left X-ray
26122-2|Femur - right X-ray
24706-4|Finger X-ray
26124-8|Finger - bilateral X-ray
30783-5|Finger fifth X-ray
37517-0|Finger fifth - bilateral X-ray
37518-8|Finger fifth - left X-ray
38147-5|Finger fifth - right X-ray
30782-7|Finger fourth X-ray
37519-6|Finger fourth - bilateral X-ray
37520-4|Finger fourth - left X-ray
38146-7|Finger fourth - right X-ray
26125-5|Finger - left X-ray
26126-3|Finger - right X-ray
30780-1|Finger second X-ray
37521-2|Finger second - bilateral X-ray
37522-0|Finger second - left X-ray
38144-2|Finger second - right X-ray
30781-9|Finger third X-ray
37523-8|Finger third - bilateral X-ray
37524-6|Finger third - left X-ray
38145-9|Finger third - right X-ray
24709-8|Foot X-ray
26127-1|Foot - bilateral X-ray
26128-9|Foot - left X-ray
26129-7|Foot - right X-ray
42399-6|Foot sesamoid bones X-ray
42400-2|Foot sesamoid bones - bilateral X-ray
43641-0|Foot sesamoid bones - left X-ray
42434-1|Foot sesamoid bones - right X-ray
37532-9|Great toe - bilateral X-ray
37533-7|Great toe - left X-ray
38152-5|Great toe - right X-ray
28582-5|Hand X-ray
36629-4|Hand - bilateral X-ray
36630-2|Hand - left X-ray
37716-8|Hand - right X-ray
24752-8|Heart Fluoroscopy video
24762-7|Hip X-ray
26130-5|Hip - bilateral X-ray
26131-3|Hip - left X-ray
26132-1|Hip - right X-ray
28567-6|Humerus X-ray
37319-1|Humerus bicipital groove X-ray
37321-7|Humerus bicipital groove - bilateral X-ray
37320-9|Humerus bicipital groove - left X-ray
38797-7|Humerus bicipital groove - right X-ray
37062-7|Humerus - bilateral X-ray
36632-8|Humerus - left X-ray
37738-2|Humerus - right X-ray
36628-6|Internal auditory canal X-ray
28565-0|Knee X-ray
36635-1|Knee - bilateral X-ray
36636-9|Knee - left X-ray
37758-0|Knee - right X-ray
48465-9|Larynx Fluoroscopy
24686-8|Lower extremity X-ray
26112-3|Lower extremity - bilateral X-ray
26113-1|Lower extremity - left X-ray
26114-9|Lower extremity - right X-ray
24829-4|Mandible X-ray
48745-4|Mandible - left X-ray
43533-9|Mandible - right X-ray
24830-2|Mastoid X-ray
26139-6|Mastoid - bilateral X-ray
26140-4|Mastoid - left X-ray
26141-2|Mastoid - right X-ray
36637-7|Maxilla X-ray
24834-4|Nasal bones X-ray
37639-2|Neck X-ray
37332-4|Olecranon - left X-ray
38798-5|Olecranon - right X-ray
24846-8|Optic foramen X-ray
26142-0|Optic foramen - bilateral X-ray
26143-8|Optic foramen - left X-ray
26144-6|Optic foramen - right X-ray
36886-0|Orbit X-ray
24854-2|Orbit - bilateral X-ray
36887-8|Orbit - left X-ray
38774-6|Orbit - right X-ray
43529-7|Orbit + Facial bones X-ray
24855-9|Oropharynx Fluoroscopy video
30791-8|Patella X-ray
36638-5|Patella - bilateral X-ray
36639-3|Patella - left X-ray
37777-0|Patella - right X-ray
28561-9|Pelvis X-ray
30885-8|Pelvis symphysis pubis X-ray
30767-8|Pelvis and Hip X-ray
30768-6|Pelvis and Hip - bilateral X-ray
36631-0|Pelvis and Hip - left X-ray
38771-2|Pelvis and Hip - right X-ray
47984-0|Pelvis and Spine Lumbar X-ray
24745-2|Petrous bone X-ray
26146-1|Radius - bilateral and Ulna - bilateral X-ray
26148-7|Radius - left and Ulna.left X-ray
26150-3|Radius - right and Ulna - right X-ray
24891-4|Radius and Ulna X-ray
24899-7|Ribs X-ray
37937-0|Ribs anterior X-ray
38073-3|Ribs anterior - bilateral X-ray
38074-1|Ribs anterior - left X-ray
37963-6|Ribs anterior - right X-ray
38868-6|Ribs anterior and posterior - left X-ray
37962-8|Ribs anterior and posterior - right X-ray
26151-1|Ribs - bilateral X-ray
69071-9|Ribs - bilateral and Chest X-ray
26152-9|Ribs - left X-ray
39326-4|Ribs - left and Chest X-ray
38866-0|Ribs lower - left X-ray
39489-0|Ribs lower posterior X-ray
42381-4|Ribs lower posterior - left X-ray
39493-2|Ribs lower posterior - right X-ray
37960-2|Ribs lower - right X-ray
37938-8|Ribs posterior X-ray
39352-0|Ribs posterior - bilateral X-ray
38869-4|Ribs posterior - left X-ray
37964-4|Ribs posterior - right X-ray
26153-7|Ribs - right X-ray
39351-2|Ribs upper anterior and posterior - left X-ray
39491-6|Ribs upper anterior and posterior - right X-ray
38867-8|Ribs upper - left X-ray
39353-8|Ribs upper posterior - left X-ray
39492-4|Ribs upper posterior - right X-ray
37961-0|Ribs upper - right X-ray
24900-3|Sacroiliac Joint X-ray
36633-6|Sacroiliac joint - bilateral X-ray
36634-4|Sacroiliac joint - left X-ray
37786-1|Sacroiliac joint - right X-ray
30884-1|Sacrum X-ray
24665-2|Sacrum and Coccyx X-ray
39058-3|Salivary gland X-ray
24903-7|Scapula X-ray
26154-5|Scapula - bilateral X-ray
26155-2|Scapula - left X-ray
26156-0|Scapula - right X-ray
42159-4|Sella turcica X-ray
24909-4|Shoulder X-ray
26157-8|Shoulder - bilateral X-ray
26158-6|Shoulder - left X-ray
26159-4|Shoulder - right X-ray
42160-2|Shunt X-ray
24911-0|Shunt Fluoroscopy
24916-9|Sinuses X-ray
28564-3|Skull X-ray
48697-7|Skull.base X-ray
37338-1|Skull and Facial bones and Mandible X-ray
24946-6|Spine Cervical X-ray
36640-1|Spine Cervical Fluoroscopy
43538-8|Spine Cervical Fluoroscopy video
37481-9|Spine Cervical and Spine Thoracic X-ray
38008-9|Spine Cervical and Thoracic and Lumbar X-ray
43781-4|Spine Cervicothoracic Junction X-ray
24972-2|Spine Lumbar X-ray
43536-2|Spine Lumbar Fluoroscopy video
24975-5|Spine.lumbar and Sacroiliac joint - bilateral X-ray
37340-7|Spine Lumbar and Sacrum X-ray
37341-5|Spine Lumbar and Sacrum and Coccyx X-ray
37342-3|Spine Lumbar and Sacrum and Sacroiliac Joint and Coccyx X-ray
46340-6|Spine Lumbosacral Junction X-ray
24983-9|Spine Thoracic X-ray
42692-4|Spine Thoracic and Lumbar X-ray
37975-0|Spine Thoracolumbar Junction X-ray
37323-3|Sternoclavicular joint - bilateral X-ray
37324-1|Sternoclavicular joint - left X-ray
37965-1|Sternoclavicular joint - right X-ray
24993-8|Sternoclavicular Joints X-ray
24994-6|Sternum X-ray
72876-6|Surgical specimen X-ray
25000-1|Temporomandibular joint X-ray
37325-8|Temporomandibular joint - bilateral X-ray
30889-0|Temporomandibular joint - left X-ray
30890-8|Temporomandibular joint - right X-ray
25006-8|Thumb X-ray
26160-2|Thumb - bilateral X-ray
26161-0|Thumb - left X-ray
26162-8|Thumb - right X-ray
26163-6|Tibia - bilateral and Fibula - bilateral X-ray
26164-4|Tibia - left and Fibula - left X-ray
26165-1|Tibia - right and Fibula - right X-ray
25011-8|Tibia and Fibula X-ray
37530-3|Toe fifth - left X-ray
38151-7|Toe fifth - right X-ray
37531-1|Toe fourth - left X-ray
38150-9|Toe fourth - right X-ray
37534-5|Toe second - left X-ray
38148-3|Toe second - right X-ray
37535-2|Toe third - left X-ray
38149-1|Toe third - right X-ray
25013-4|Toes X-ray
26166-9|Toes - bilateral X-ray
26167-7|Toes - left X-ray
26168-5|Toes - right X-ray
48464-2|Trachea Fluoroscopy
24689-2|Upper extremity X-ray
26115-6|Upper extremity - bilateral X-ray
26116-4|Upper extremity - left X-ray
26117-2|Upper extremity - right X-ray
24619-9|Wrist X-ray
26169-3|Wrist - bilateral X-ray
26170-1|Wrist - left X-ray
51392-9|Wrist - left and Hand - left X-ray
26171-9|Wrist - right X-ray
51388-7|Wrist - right and Hand - right X-ray
43468-8|Unspecified body region X-ray
49512-7|Unspecified body region Fluoroscopy
25074-6|Zygomatic arch X-ray
26172-7|Zygomatic arch - bilateral X-ray
26173-5|Zygomatic arch - left X-ray
26174-3|Zygomatic arch - right X-ray
51387-9|Knee - bilateral X-ray and (AP view standing)
39370-2|Ankle - right X-ray and (view W manual stress)
30635-7|Gastrointestine upper Fluoroscopy and AP W contrast PO
42162-8|Gastrointestine upper Fluoroscopy and AP W water soluble contrast PO
39400-7|Wrist - right X-ray and carpal tunnel
69131-1|Hip X-ray and Danelius Miller
69140-2|Hip - left X-ray and Danelius Miller
39513-7|Hip - right X-ray and Danelius Miller
39360-3|Pelvis X-ray and inlet and outlet
69059-4|Hip - bilateral X-ray and lateral crosstable
69139-4|Hip - left X-ray and lateral crosstable
39377-7|Hip - right X-ray and lateral crosstable
37583-2|Pelvis and Hip - bilateral X-ray and lateral frog
39372-8|Ankle - right X-ray and Mortise
39373-6|Elbow - right X-ray and oblique
39390-0|Knee - right X-ray and oblique
39511-1|Pelvis X-ray and oblique
39376-9|Radius - right and Ulna - right X-ray and oblique
42164-4|Spine Cervical X-ray and oblique
42163-6|Spine Lumbar X-ray and oblique
39414-8|Spine Thoracic X-ray and oblique
39398-3|Tibia - right and Fibula - right X-ray and oblique
69056-0|Elbow - bilateral X-ray and obliques
41811-1|Ribs - bilateral and Chest X-ray and PA chest
41832-7|Ribs - left and Chest X-ray and PA chest
42010-9|Ribs - right and Chest X-ray and PA chest
42165-1|Ribs and Chest X-ray and PA chest
46389-3|Elbow - bilateral X-ray and radial head capitellar
39391-8|Knee - right X-ray and Sunrise
39412-2|Spine Thoracic X-ray and Swimmers
69148-5|Knee - left X-ray and tunnel
39389-2|Knee - right X-ray and tunnel
30694-4|Thyroid Scan and uptake.single
42271-7|Thyroid Scan and uptake W I-123 IV
60527-9|Thyroid Scan and uptake W I-123 PO
25008-4|Thyroid Scan and uptake W I-131 IV
69236-8|Thyroid Scan and uptake W I-131 PO
43672-5|Thyroid Scan and uptake
44147-7|Thyroid Scan and uptake W Tc-99m pertechnetate IV
42405-1|Knee X-ray (AP^standing) and (lateral^W hyperextension)
42401-0|Spine Lumbar X-ray (AP W R-bending and W L-bending and WO bending) and Lateral
42411-9|Spine Lumbar X-ray (AP^W R-bending and W L-bending) and (lateral^W flexion and W extension)
39392-6|Shoulder - right X-ray (W internal rotation and W external rotation) and axillary
44199-8|Facial bones X-ray 1 or 2 views
44198-0|Knee X-ray 1 or 2 views
47373-6|Knee - left X-ray 1 or 2 views
47375-1|Knee - right X-ray 1 or 2 views
43521-4|Mandible X-ray 1 or 2 views
47983-2|Mastoid - bilateral X-ray 1 or 2 views
48489-9|Mastoid - left X-ray 1 or 2 views
48488-1|Mastoid - right X-ray 1 or 2 views
43522-2|Pelvis X-ray 1 or 2 views
48467-5|Sacroiliac Joint X-ray 1 or 2 views
43523-0|Sinuses X-ray 1 or 2 views
44202-0|Knee X-ray 1 or 2 views portable
44201-2|Pelvis X-ray 1 or 2 views portable
36641-9|Abdomen X-ray 2 views
37064-3|Acetabulum - left X-ray 2 views
37664-0|Acetabulum - right X-ray 2 views
36665-8|Acromioclavicular joint - left X-ray 2 views
37661-6|Acromioclavicular joint - right X-ray 2 views
24540-7|Ankle X-ray 2 views
26385-5|Ankle - bilateral X-ray 2 views
26386-3|Ankle - left X-ray 2 views
26387-1|Ankle - right X-ray 2 views
36642-7|Breast - left Mammogram 2 views
37768-9|Breast - right Mammogram 2 views
36661-7|Calcaneus X-ray 2 views
48433-7|Calcaneus - bilateral X-ray 2 views
36662-5|Calcaneus - left X-ray 2 views
37718-4|Calcaneus - right X-ray 2 views
36643-5|Chest X-ray 2 views
36644-3|Chest Fluoroscopy 2 views
36645-0|Clavicle X-ray 2 views
36646-8|Clavicle - left X-ray 2 views
37679-8|Clavicle - right X-ray 2 views
36647-6|Coccyx X-ray 2 views
36648-4|Elbow X-ray 2 views
36649-2|Elbow - bilateral X-ray 2 views
36650-0|Elbow - left X-ray 2 views
37681-4|Elbow - right X-ray 2 views
36652-6|Femur X-ray 2 views
36653-4|Femur - bilateral X-ray 2 views
36654-2|Femur - left X-ray 2 views
37690-5|Femur - right X-ray 2 views
36655-9|Finger X-ray 2 views
36656-7|Finger - left X-ray 2 views
37694-7|Finger - right X-ray 2 views
30784-3|Foot X-ray 2 views
36657-5|Foot - bilateral X-ray 2 views
38846-2|Foot - left X-ray 2 views
37697-0|Foot - right X-ray 2 views
24721-3|Hand X-ray 2 views
26388-9|Hand - bilateral X-ray 2 views
26389-7|Hand - left X-ray 2 views
26390-5|Hand - right X-ray 2 views
36663-3|Hip X-ray 2 views
69058-6|Hip - bilateral X-ray 2 views
36664-1|Hip - left X-ray 2 views
37721-8|Hip - right X-ray 2 views
24765-0|Humerus X-ray 2 views
26391-3|Humerus - bilateral X-ray 2 views
26392-1|Humerus - left X-ray 2 views
26393-9|Humerus - right X-ray 2 views
24806-2|Knee X-ray 2 views
26394-7|Knee - bilateral X-ray 2 views
26395-4|Knee - left X-ray 2 views
26396-2|Knee - right X-ray 2 views
36651-8|Lower extremity X-ray 2 views
69257-4|Lower extremity - right X-ray 2 views
24861-7|Patella X-ray 2 views
26397-0|Patella - bilateral X-ray 2 views
26398-8|Patella - left X-ray 2 views
26399-6|Patella - right X-ray 2 views
37617-8|Pelvis X-ray 2 views
42685-8|Pelvis and Hip - left X-ray 2 views
42686-6|Pelvis and Hip - right X-ray 2 views
36659-1|Radius - bilateral and Ulna - bilateral X-ray 2 views
36660-9|Radius - left and Ulna.left X-ray 2 views
37707-7|Radius - right and Ulna - right X-ray 2 views
36658-3|Radius and Ulna X-ray 2 views
39060-9|Ribs X-ray 2 views
42687-4|Ribs - bilateral X-ray 2 views
37066-8|Ribs - left X-ray 2 views
37780-4|Ribs - right X-ray 2 views
37651-7|Sacrum X-ray 2 views
44179-0|Sacrum and Coccyx X-ray 2 views
37655-8|Scapula X-ray 2 views
36666-6|Scapula - left X-ray 2 views
37787-9|Scapula - right X-ray 2 views
42435-8|Sella turcica X-ray 2 views
37840-6|Shoulder X-ray 2 views
36667-4|Shoulder - bilateral X-ray 2 views
36668-2|Shoulder - left X-ray 2 views
37793-7|Shoulder - right X-ray 2 views
37853-9|Sinuses X-ray 2 views
37867-9|Skull X-ray 2 views
36669-0|Spine Cervical X-ray 2 views
43784-8|Spine Cervical and Thoracic and Lumbar X-ray 2 views
36670-8|Spine Lumbar X-ray 2 views
37905-7|Spine Thoracic X-ray 2 views
24984-7|Spine Thoracic and Lumbar X-ray 2 views
69273-1|Spine Thoracolumbar Junction X-ray 2 views
37883-6|Sternum X-ray 2 views
36671-6|Tibia - bilateral and Fibula - bilateral X-ray 2 views
36672-4|Tibia - left and Fibula - left X-ray 2 views
37815-8|Tibia - right and Fibula - right X-ray 2 views
37895-0|Tibia and Fibula X-ray 2 views
37902-4|Toes X-ray 2 views
37348-0|Toes - bilateral X-ray 2 views
36673-2|Toes - left X-ray 2 views
37821-6|Toes - right X-ray 2 views
37922-2|Upper extremity X-ray 2 views
37925-5|Wrist X-ray 2 views
37482-7|Wrist - bilateral X-ray 2 views
37483-5|Wrist - left X-ray 2 views
37826-5|Wrist - right X-ray 2 views
69305-1|Zygomatic arch X-ray 2 views
42430-9|Knee - right X-ray 2 views and (views standing)
42009-1|Chest X-ray 2 views and apical
39378-5|Knee - right X-ray 2 views and oblique
48468-3|Ribs - bilateral and Chest X-ray 2 views and PA chest
43467-0|Chest X-ray 2 views and right oblique and left oblique
69060-2|Knee - bilateral X-ray 2 views and Sunrise
69142-8|Knee - left X-ray 2 views and Sunrise
39379-3|Knee - right X-ray 2 views and Sunrise
39380-1|Knee - right X-ray 2 views and Sunrise and tunnel
69061-0|Knee - bilateral X-ray 2 views and tunnel
41819-4|Knee - left X-ray 2 views and tunnel
39381-9|Knee - right X-ray 2 views and tunnel
69143-6|Knee - left X-ray 2 views and tunnel standing
39382-7|Knee - right X-ray 2 views and tunnel standing
38118-6|Neck X-ray 2 views lateral
38844-7|Elbow - left X-ray 2 views Oblique
37686-3|Elbow - right X-ray 2 views Oblique
38871-0|Knee - left X-ray 2 views Oblique
38108-7|Knee - right X-ray 2 views Oblique
38874-4|Tibia - left and Fibula - left X-ray 2 views Oblique
38114-5|Tibia - right and Fibula - right X-ray 2 views Oblique
44181-6|Sacroiliac Joint X-ray 2 or 3 views
43539-6|Spine Cervical X-ray 2 or 3 views
48469-1|Spine Lumbar X-ray 2 or 3 views
39880-0|Bone Scan 2 views phase
44184-0|Elbow X-ray 2 views portable
44182-4|Hand X-ray 2 views portable
44183-2|Radius and Ulna X-ray 2 views portable
36674-0|Spine Lumbar X-ray 2 views portable
37658-2|Spine Thoracic and Lumbar X-ray 2 views scoliosis
38843-9|Wrist - left X-ray 2 views tunnel.carpal
37678-0|Wrist - right X-ray 2 views tunnel.carpal
42166-9|Heart Scan 2 views at rest and W Tl-201 IV
38841-3|Ankle - left X-ray 2 views standing
37675-6|Ankle - right X-ray 2 views standing
37068-4|Foot - bilateral X-ray 2 views standing
37069-2|Foot - left X-ray 2 views standing
37698-8|Foot - right X-ray 2 views standing
36945-4|Knee - bilateral X-ray 2 views standing
38851-2|Knee - left X-ray 2 views standing
37762-2|Knee - right X-ray 2 views standing
36946-2|Spine Lumbar X-ray 2 views standing
69274-9|Spine Thoracic X-ray 2 views standing
38840-5|Ankle - left X-ray 2 views W manual stress
37672-3|Ankle - right X-ray 2 views W manual stress
37067-6|Chest X-ray 2 views W nipple markers
36293-9|Abdomen X-ray 3 views
37635-0|Acetabulum X-ray 3 views
36294-7|Ankle X-ray 3 views
36295-4|Ankle - bilateral X-ray 3 views
36296-2|Ankle - left X-ray 3 views
37665-7|Ankle - right X-ray 3 views
36298-8|Chest X-ray 3 views
36299-6|Elbow X-ray 3 views
36300-2|Elbow - bilateral X-ray 3 views
36301-0|Elbow - left X-ray 3 views
37682-2|Elbow - right X-ray 3 views
36297-0|Facial bones X-ray 3 views
36302-8|Femur X-ray 3 views
36303-6|Finger X-ray 3 views
36304-4|Finger - left X-ray 3 views
37695-4|Finger - right X-ray 3 views
36305-1|Foot X-ray 3 views
36306-9|Foot - bilateral X-ray 3 views
36307-7|Foot - left X-ray 3 views
37699-6|Foot - right X-ray 3 views
24722-1|Hand X-ray 3 views
26379-8|Hand - bilateral X-ray 3 views
26380-6|Hand - left X-ray 3 views
26381-4|Hand - right X-ray 3 views
36308-5|Hip - bilateral X-ray 3 views
36309-3|Hip - left X-ray 3 views
37722-6|Hip - right X-ray 3 views
30788-4|Knee X-ray 3 views
36310-1|Knee - bilateral X-ray 3 views
36311-9|Knee - left X-ray 3 views
37742-4|Knee - right X-ray 3 views
36312-7|Mandible X-ray 3 views
36838-1|Mastoid X-ray 3 views
48470-9|Mastoid - left X-ray 3 views
48471-7|Mastoid - right X-ray 3 views
37604-6|Nasal bones X-ray 3 views
69261-6|Patella - right X-ray 3 views
30766-0|Pelvis X-ray 3 views
37256-5|Pelvis and Spine Lumbar X-ray 3 views
39062-5|Ribs X-ray 3 views
36313-5|Ribs - bilateral X-ray 3 views
36314-3|Ribs - left X-ray 3 views
37781-2|Ribs - right X-ray 3 views
37648-3|Sacroiliac Joint X-ray 3 views
39061-7|Sacrum and Coccyx X-ray 3 views
24908-6|Shoulder X-ray 3 views
26382-2|Shoulder - bilateral X-ray 3 views
26383-0|Shoulder - left X-ray 3 views
26384-8|Shoulder - right X-ray 3 views
37854-7|Sinuses X-ray 3 views
24918-5|Skull X-ray 3 views
24941-7|Spine Cervical X-ray 3 views
30775-1|Spine Lumbar X-ray 3 views
37257-3|Spine Lumbar and Sacroiliac Joint X-ray 3 views
37259-9|Spine Lumbar and Sacrum X-ray 3 views
37260-7|Spine Lumbar and Sacrum and Coccyx X-ray 3 views
37261-5|Spine Lumbar and Sacrum and Sacroiliac Joint and Coccyx X-ray 3 views
37906-5|Spine Thoracic X-ray 3 views
37881-0|Sternoclavicular Joint X-ray 3 views
37888-5|Thumb X-ray 3 views
36315-0|Thumb - left X-ray 3 views
37812-5|Thumb - right X-ray 3 views
36316-8|Toes - left X-ray 3 views
37820-8|Toes - right X-ray 3 views
37926-3|Wrist X-ray 3 views
37454-6|Wrist - bilateral X-ray 3 views
48738-9|Wrist - bilateral and Hand - bilateral X-ray 3 views
37455-3|Wrist - left X-ray 3 views
37827-3|Wrist - right X-ray 3 views
48737-1|Wrist and Hand X-ray 3 views
37933-9|Zygomatic arch X-ray 3 views
69154-3|Shoulder - left X-ray 3 views and axillary
39393-4|Shoulder - right X-ray 3 views and axillary
39399-1|Wrist - right X-ray 3 views and carpal tunnel
39364-5|Wrist - right X-ray 3 views and radial deviation
39404-9|Sinuses X-ray 3 views and submentovertex
39383-5|Knee - right X-ray 3 views and Sunrise
48472-5|Spine Thoracic X-ray 3 views and Swimmers
39365-2|Wrist - right X-ray 3 views and ulnar deviation
69155-0|Shoulder - left X-ray 3 views and Y
39394-2|Shoulder - right X-ray 3 views and Y
43499-3|Foot - left X-ray 3 or 4 views
43483-7|Foot - right X-ray 3 or 4 views
39901-4|Bone Scan 3 views phase multiple areas
39902-2|Bone Scan 3 views phase single area
39882-6|Bone Scan 3 views phase whole body
39883-4|Bone Scan 3 views phase
30776-9|Spine Lumbar X-ray 3 views portable
69151-9|Wrist - left X-ray 3 views scaphoid
24778-3|Kidney - bilateral X-ray 3 views serial W and WO contrast IV
69138-6|Ankle - left X-ray 3 views standing
69254-1|Ankle - right X-ray 3 views standing
36947-0|Foot - bilateral X-ray 3 views standing
36948-8|Foot - left X-ray 3 views standing
37700-2|Foot - right X-ray 3 views standing
36949-6|Spine Lumbar X-ray 3 views standing
42443-2|Spine Thoracic X-ray 3 views standing
36317-6|Ankle X-ray 4 views
36319-2|Breast Mammogram 4 views
36320-0|Chest X-ray 4 views
36321-8|Chest Fluoroscopy 4 views
36322-6|Elbow - bilateral X-ray 4 views
36323-4|Elbow - left X-ray 4 views
37683-0|Elbow - right X-ray 4 views
36318-4|Facial bones X-ray 4 views
36324-2|Femur - left X-ray 4 views
37691-3|Femur - right X-ray 4 views
30789-2|Knee X-ray 4 views
36325-9|Knee - bilateral X-ray 4 views
36326-7|Knee - left X-ray 4 views
37743-2|Knee - right X-ray 4 views
36327-5|Mandible X-ray 4 views
43534-7|Mandible - left X-ray 4 views
43535-4|Mandible - right X-ray 4 views
36839-9|Mastoid X-ray 4 views
37609-5|Optic foramen X-ray 4 views
37612-9|Orbit - bilateral X-ray 4 views
36328-3|Ribs - bilateral X-ray 4 views
69265-7|Shoulder X-ray 4 views
36329-1|Shoulder - bilateral X-ray 4 views
36330-9|Shoulder - left X-ray 4 views
37794-5|Shoulder - right X-ray 4 views
37855-4|Sinuses X-ray 4 views
37868-7|Skull X-ray 4 views
36331-7|Spine Cervical X-ray 4 views
36332-5|Spine Lumbar X-ray 4 views
48473-3|Spine Lumbar and Sacrum X-ray 4 views
37907-3|Spine Thoracic X-ray 4 views
37882-8|Sternoclavicular Joint X-ray 4 views
38155-8|Wrist X-ray 4 views
37070-0|Wrist - bilateral X-ray 4 views
37071-8|Wrist - left X-ray 4 views
37828-1|Wrist - right X-ray 4 views
37934-7|Zygomatic arch X-ray 4 views
69144-4|Knee - left X-ray 4 views and AP standing
39384-3|Knee - right X-ray 4 views and AP standing
39385-0|Knee - right X-ray 4 views and oblique
39413-0|Spine Thoracic X-ray 4 views and oblique
39099-7|Ribs - bilateral and Chest X-ray 4 views and PA chest
69063-6|Knee - bilateral X-ray 4 views and Sunrise and tunnel
39387-6|Knee - right X-ray 4 views and Sunrise and tunnel
69145-1|Knee - left X-ray 4 views and tunnel
39386-8|Knee - right X-ray 4 views and tunnel
69062-8|Knee - bilateral X-ray 4 views standing
38852-0|Knee - left X-ray 4 views standing
37763-0|Knee - right X-ray 4 views standing
36675-7|Facial bones X-ray 5 views
36676-5|Knee - left X-ray 5 views
37744-0|Knee - right X-ray 5 views
36890-2|Mastoid X-ray 5 views
37351-4|Pelvis and Spine Lumbar X-ray 5 views
30750-4|Shoulder X-ray 5 views
36677-3|Shoulder - left X-ray 5 views
37795-2|Shoulder - right X-ray 5 views
37856-2|Sinuses X-ray 5 views
24922-7|Skull X-ray 5 views
24939-1|Spine Cervical X-ray 5 views
30797-5|Spine Lumbar X-ray 5 views
37353-0|Spine Lumbar and Sacroiliac Joint X-ray 5 views
37355-5|Spine Lumbar and Sacrum X-ray 5 views
37356-3|Spine Lumbar and Sacrum and Coccyx X-ray 5 views
37357-1|Spine Lumbar and Sacrum and Sacroiliac Joint and Coccyx X-ray 5 views
37350-6|Temporomandibular joint - bilateral X-ray 5 views
37072-6|Wrist - left X-ray 5 views
37829-9|Wrist - right X-ray 5 views
39407-2|Spine Thoracic X-ray 5 views and oblique
69081-8|Spine Cervical X-ray 5 views and Swimmers
37073-4|Spine Lumbar X-ray 5 views standing
69080-0|Spine Cervical X-ray 5 views W flexion and W extension
39063-3|Spine Lumbar X-ray 5 views W flexion and W extension
42273-3|Ankle - bilateral X-ray 6 views
36678-1|Knee - bilateral X-ray 6 views
36679-9|Shoulder - left X-ray 6 views
37796-0|Shoulder - right X-ray 6 views
42691-6|Spine Cervical X-ray 6 views
38156-6|Wrist X-ray 6 views
37074-2|Wrist - left X-ray 6 views
37830-7|Wrist - right X-ray 6 views
36680-7|Spine Cervical X-ray 7 views
36681-5|Spine Lumbar X-ray 7 views
36682-3|Knee - bilateral X-ray 8 views
36683-1|Wrist - left X-ray 8 views
37831-5|Wrist - right X-ray 8 views
42412-7|Shoulder - left X-ray 90 degree abduction
39064-1|Ribs X-ray anterior and lateral
69070-1|Ribs - bilateral X-ray anterior and lateral
38856-1|Ribs - left X-ray anterior and lateral
37782-0|Ribs - right X-ray anterior and lateral
24796-5|Abdomen X-ray AP and AP left lateral-decubitus
24792-4|Abdomen X-ray AP and AP left lateral-decubitus portable
24653-8|Chest X-ray AP and AP right lateral-decubitus
24654-6|Chest X-ray AP and AP right lateral-decubitus portable
37080-9|Shoulder - bilateral X-ray AP and axillary
37081-7|Shoulder - bilateral X-ray AP and axillary and outlet
37082-5|Shoulder - left X-ray AP and axillary and outlet
38781-1|Shoulder - right X-ray AP and axillary and outlet
39339-7|Shoulder - bilateral X-ray AP and axillary and outlet and 30 degree caudal angle
37083-3|Shoulder - left X-ray AP and axillary and outlet and Zanca
38782-9|Shoulder - right X-ray AP and axillary and outlet and Zanca
37126-0|Shoulder - bilateral X-ray AP and axillary and Y
37084-1|Shoulder - left X-ray AP and axillary and Y
38783-7|Shoulder - right X-ray AP and axillary and Y
39512-9|Hip - right X-ray AP and Danelius Miller
39401-5|Shoulder X-ray AP and Grashey and axillary
69153-5|Shoulder - left X-ray AP and Grashey and axillary
69262-4|Shoulder - right X-ray AP and Grashey and axillary
37618-6|Pelvis X-ray AP and inlet
37623-6|Pelvis X-ray AP and inlet and outlet
39065-8|Pelvis X-ray AP and inlet and outlet and oblique
37619-4|Pelvis X-ray AP and Judet
24794-0|Abdomen X-ray AP and lateral
30779-3|Ankle X-ray AP and lateral
36684-9|Ankle - bilateral X-ray AP and lateral
36685-6|Ankle - left X-ray AP and lateral
37667-3|Ankle - right X-ray AP and lateral
36686-4|Calcaneus - bilateral X-ray AP and lateral
36701-1|Calcaneus - left X-ray AP and lateral
37719-2|Calcaneus - right X-ray AP and lateral
36687-2|Chest X-ray AP and lateral
39066-6|Chest Fluoroscopy AP and lateral
36688-0|Coccyx X-ray AP and lateral
36689-8|Elbow X-ray AP and lateral
36690-6|Elbow - bilateral X-ray AP and lateral
36691-4|Elbow - left X-ray AP and lateral
37684-8|Elbow - right X-ray AP and lateral
36693-0|Femur X-ray AP and lateral
36694-8|Femur - bilateral X-ray AP and lateral
36695-5|Femur - left X-ray AP and lateral
37692-1|Femur - right X-ray AP and lateral
39069-0|Foot X-ray AP and lateral
36696-3|Foot - bilateral X-ray AP and lateral
36697-1|Foot - left X-ray AP and lateral
37701-0|Foot - right X-ray AP and lateral
42409-3|Foot sesamoid bones X-ray AP and lateral
69130-3|Hand X-ray AP and lateral
48474-1|Hand - bilateral X-ray AP and lateral
38847-0|Hand - left X-ray AP and lateral
37710-1|Hand - right X-ray AP and lateral
36702-9|Hip X-ray AP and lateral
36703-7|Hip - bilateral X-ray AP and lateral
36704-5|Hip - left X-ray AP and lateral
37725-9|Hip - right X-ray AP and lateral
36706-0|Humerus X-ray AP and lateral
36707-8|Humerus - bilateral X-ray AP and lateral
36708-6|Humerus - left X-ray AP and lateral
37736-6|Humerus - right X-ray AP and lateral
36709-4|Knee X-ray AP and lateral
36590-8|Knee - bilateral X-ray AP and lateral
36710-2|Knee - left X-ray AP and lateral
37745-7|Knee - right X-ray AP and lateral
36692-2|Lower extremity X-ray AP and lateral
69258-2|Lower extremity - right X-ray AP and lateral
36711-0|Mandible X-ray AP and lateral
42438-2|Neck X-ray AP and lateral
36712-8|Patella - bilateral X-ray AP and lateral
36713-6|Patella - left X-ray AP and lateral
37776-2|Patella - right X-ray AP and lateral
37620-2|Pelvis X-ray AP and lateral
36705-2|Pelvis and Hip X-ray AP and lateral
36699-7|Radius - bilateral and Ulna - bilateral X-ray AP and lateral
36700-3|Radius - left and Ulna.left X-ray AP and lateral
37708-5|Radius - right and Ulna - right X-ray AP and lateral
36698-9|Radius and Ulna X-ray AP and lateral
37652-5|Sacrum X-ray AP and lateral
36714-4|Scapula - bilateral X-ray AP and lateral
36715-1|Scapula - left X-ray AP and lateral
37788-7|Scapula - right X-ray AP and lateral
37841-4|Shoulder X-ray AP and lateral
36716-9|Shoulder - bilateral X-ray AP and lateral
24919-3|Skull X-ray AP and lateral
24942-5|Spine Cervical X-ray AP and lateral
37361-3|Spine Cervical and Spine Thoracic X-ray AP and lateral
39067-4|Spine Cervical and Thoracic and Lumbar X-ray AP and lateral
43785-5|Spine Cervicothoracic Junction X-ray AP and lateral
24970-6|Spine Lumbar X-ray AP and lateral
30753-8|Spine Thoracic X-ray AP and lateral
38123-6|Spine Thoracic and Lumbar X-ray AP and lateral
37974-3|Spine Thoracolumbar Junction X-ray AP and lateral
37889-3|Thumb X-ray AP and lateral
36717-7|Tibia - bilateral and Fibula - bilateral X-ray AP and lateral
36718-5|Tibia - left and Fibula - left X-ray AP and lateral
37816-6|Tibia - right and Fibula - right X-ray AP and lateral
37896-8|Tibia and Fibula X-ray AP and lateral
36719-3|Toes - left X-ray AP and lateral
37822-4|Toes - right X-ray AP and lateral
30793-4|Wrist X-ray AP and lateral
38860-3|Wrist - left X-ray AP and lateral
37832-3|Wrist - right X-ray AP and lateral
37839-8|Shoulder X-ray AP and lateral and axillary
39070-8|Chest X-ray AP and lateral and lordotic
42404-4|Hip - left X-ray AP and lateral and measurement
39071-6|Knee X-ray AP and lateral and Merchants
37095-7|Ankle X-ray AP and lateral and Mortise
37096-5|Ankle - bilateral X-ray AP and lateral and Mortise
37097-3|Ankle - left X-ray AP and lateral and Mortise
37666-5|Ankle - right X-ray AP and lateral and Mortise
39072-4|Ankle X-ray AP and lateral and oblique
36720-1|Ankle - bilateral X-ray AP and lateral and oblique
36721-9|Ankle - left X-ray AP and lateral and oblique
37668-1|Ankle - right X-ray AP and lateral and oblique
36731-8|Calcaneus X-ray AP and lateral and oblique
36722-7|Elbow X-ray AP and lateral and oblique
36723-5|Elbow - bilateral X-ray AP and lateral and oblique
36724-3|Elbow - left X-ray AP and lateral and oblique
37685-5|Elbow - right X-ray AP and lateral and oblique
36725-0|Finger X-ray AP and lateral and oblique
36726-8|Finger - bilateral X-ray AP and lateral and oblique
36727-6|Finger - left X-ray AP and lateral and oblique
37696-2|Finger - right X-ray AP and lateral and oblique
36728-4|Foot X-ray AP and lateral and oblique
36729-2|Foot - bilateral X-ray AP and lateral and oblique
36730-0|Foot - left X-ray AP and lateral and oblique
37702-8|Foot - right X-ray AP and lateral and oblique
69057-8|Hand - bilateral X-ray AP and lateral and oblique
38848-8|Hand - left X-ray AP and lateral and oblique
37711-9|Hand - right X-ray AP and lateral and oblique
36732-6|Knee - bilateral X-ray AP and lateral and oblique
36733-4|Knee - left X-ray AP and lateral and oblique
37748-1|Knee - right X-ray AP and lateral and oblique
37624-4|Pelvis X-ray AP and lateral and oblique
36734-2|Spine Cervical X-ray AP and lateral and oblique
36735-9|Spine Lumbar X-ray AP and lateral and oblique
37908-1|Spine Thoracic X-ray AP and lateral and oblique
36736-7|Thumb - left X-ray AP and lateral and oblique
37813-3|Thumb - right X-ray AP and lateral and oblique
37927-1|Wrist X-ray AP and lateral and oblique
37099-9|Spine Cervical X-ray AP and lateral and oblique and odontoid
38083-2|Spine Cervical X-ray AP and lateral and oblique and odontoid and swimmer
37101-3|Spine Lumbar X-ray AP and lateral and oblique and spot
42410-1|Spine Lumbar X-ray AP and lateral and oblique and spot standing
37102-1|Knee - bilateral X-ray AP and lateral and oblique and Sunrise
37118-7|Knee - bilateral X-ray AP and lateral and oblique and Sunrise and tunnel
37115-3|Knee X-ray AP and lateral and oblique and tunnel
69137-8|Ankle - left X-ray AP and lateral and oblique standing
39371-0|Ankle - right X-ray AP and lateral and oblique standing
39334-8|Foot - left X-ray AP and lateral and oblique standing
39375-1|Foot - right X-ray AP and lateral and oblique standing
42417-6|Ankle - bilateral X-ray AP and lateral and oblique W manual stress
42418-4|Ankle - left X-ray AP and lateral and oblique W manual stress
39369-4|Ankle - right X-ray AP and lateral and oblique W manual stress
37103-9|Spine Cervical X-ray AP and lateral and odontoid
37079-1|Spine Cervical X-ray AP and lateral and odontoid portable
39074-0|Chest X-ray AP and lateral and right oblique and left oblique
39073-2|Knee X-ray AP and lateral and right oblique and left oblique
69147-7|Knee - left X-ray AP and lateral and right oblique and left oblique
39388-4|Knee - right X-ray AP and lateral and right oblique and left oblique
37105-4|Spine Lumbar X-ray AP and lateral and spot
37106-2|Knee X-ray AP and lateral and Sunrise
37107-0|Knee - bilateral X-ray AP and lateral and Sunrise
37108-8|Knee - left X-ray AP and lateral and Sunrise
37749-9|Knee - right X-ray AP and lateral and Sunrise
37109-6|Patella - bilateral X-ray AP and lateral and Sunrise
37110-4|Patella - left X-ray AP and lateral and Sunrise
38786-0|Patella - right X-ray AP and lateral and Sunrise
37111-2|Knee X-ray AP and lateral and Sunrise and tunnel
37116-1|Knee - bilateral X-ray AP and lateral and Sunrise and tunnel
37117-9|Knee - left X-ray AP and lateral and Sunrise and tunnel
37740-8|Knee - right X-ray AP and lateral and Sunrise and tunnel
38009-7|Spine Thoracic X-ray AP and lateral and Swimmers
37112-0|Knee X-ray AP and lateral and tunnel
37113-8|Knee - bilateral X-ray AP and lateral and tunnel
37114-6|Knee - left X-ray AP and lateral and tunnel
37747-3|Knee - right X-ray AP and lateral and tunnel
69065-1|Abdomen X-ray AP and lateral crosstable
37086-6|Hip X-ray AP and lateral crosstable
37087-4|Hip - left X-ray AP and lateral crosstable
37723-4|Hip - right X-ray AP and lateral crosstable
37090-8|Knee X-ray AP and lateral crosstable
69146-9|Knee - left X-ray AP and lateral crosstable
37089-0|Pelvis and Hip X-ray AP and lateral crosstable
37088-2|Pelvis and Hip - left X-ray AP and lateral crosstable
38784-5|Pelvis and Hip - right X-ray AP and lateral crosstable
30763-7|Abdomen X-ray AP and lateral crosstable portable
37077-5|Hip X-ray AP and lateral crosstable portable
37091-6|Hip X-ray AP and lateral frog
37092-4|Hip - bilateral X-ray AP and lateral frog
37093-2|Hip - left X-ray AP and lateral frog
37724-2|Hip - right X-ray AP and lateral frog
30770-2|Pelvis and Hip X-ray AP and lateral frog
42167-7|Pelvis and Hip - bilateral X-ray AP and lateral frog
37094-0|Pelvis and Hip - left X-ray AP and lateral frog
38785-2|Pelvis and Hip - right X-ray AP and lateral frog
41776-6|Pelvis and Hip - right X-ray AP and lateral frog portable
24793-2|Abdomen X-ray AP and lateral portable
44185-7|Femur X-ray AP and lateral portable
44186-5|Foot X-ray AP and lateral portable
41817-8|Hip - left X-ray AP and lateral portable
41777-4|Hip - right X-ray AP and lateral portable
30726-4|Spine Cervical X-ray AP and lateral portable
37078-3|Spine Lumbar X-ray AP and lateral portable
30754-6|Spine Thoracic X-ray AP and lateral portable
39330-6|Ankle - bilateral X-ray AP and lateral standing
42380-6|Ankle - left X-ray AP and lateral standing
39368-6|Ankle - right X-ray AP and lateral standing
39068-2|Foot X-ray AP and lateral standing
39331-4|Foot - bilateral X-ray AP and lateral standing
39332-2|Foot - left X-ray AP and lateral standing
39374-4|Foot - right X-ray AP and lateral standing
24805-4|Knee X-ray AP and lateral standing
26364-0|Knee - bilateral X-ray AP and lateral standing
26365-7|Knee - left X-ray AP and lateral standing
26366-5|Knee - right X-ray AP and lateral standing
39333-0|Spine Lumbar X-ray AP and lateral standing
38084-0|Abdomen X-ray AP and left posterior oblique
37119-5|Abdomen X-ray AP and oblique
39076-5|Foot X-ray AP and oblique
37621-0|Pelvis X-ray AP and oblique
37649-1|Sacroiliac Joint X-ray AP and oblique
39075-7|Toes X-ray AP and oblique
37098-1|Spine Cervical X-ray AP and oblique and lateral W flexion and W extension
44187-3|Spine Cervical X-ray AP and oblique and odontoid and lateral portable W flexion and W extension
37100-5|Spine Cervical X-ray AP and oblique and odontoid and lateral W flexion and W extension
24797-3|Abdomen X-ray AP and oblique prone
37120-3|Spine Cervical X-ray AP and odontoid and lateral crosstable
37104-7|Spine Cervical X-ray AP and odontoid and lateral W flexion and W extension
42011-7|Chest and Abdomen X-ray AP and PA chest
24642-1|Chest X-ray AP and PA upright
24808-8|Knee X-ray AP and PA standing
26361-6|Knee - bilateral X-ray AP and PA standing
26362-4|Knee - left X-ray AP and PA standing
26363-2|Knee - right X-ray AP and PA standing
37121-1|Clavicle - left X-ray AP and Serendipity
37680-6|Clavicle - right X-ray AP and Serendipity
37122-9|Shoulder - left X-ray AP and Stryker Notch
37797-8|Shoulder - right X-ray AP and Stryker Notch
37485-0|Humerus X-ray AP and transthoracic
39077-3|Shoulder X-ray AP and transthoracic
46349-7|Shoulder - bilateral X-ray AP and transthoracic
38082-4|Shoulder - left X-ray AP and transthoracic
38822-3|Shoulder - right X-ray AP and transthoracic
37123-7|Shoulder - left X-ray AP and West Point
38787-8|Shoulder - right X-ray AP and West Point
36961-1|Shoulder - left X-ray AP and West Point and outlet
37799-4|Shoulder - right X-ray AP and West Point and outlet
37124-5|Scapula - left X-ray AP and Y
37789-5|Scapula - right X-ray AP and Y
69266-5|Shoulder X-ray AP and Y
37125-2|Shoulder - left X-ray AP and Y
38788-6|Shoulder - right X-ray AP and Y
24562-1|Abdomen X-ray AP (left lateral-decubitus and right lateral-decubitus)
24650-4|Chest X-ray AP (right lateral-decubitus and left lateral-decubitus)
24649-6|Chest X-ray AP (right lateral-decubitus and left lateral-decubitus) portable
37085-8|Abdomen X-ray AP (supine and lateral-decubitus)
37076-7|Abdomen X-ray AP (supine and lateral-decubitus) portable
24798-1|Abdomen X-ray AP (supine and upright)
43463-9|Chest and Abdomen X-ray AP (supine and upright) and PA chest
24795-7|Abdomen X-ray AP (supine and upright) portable
42019-0|Abdomen X-ray AP (upright and left lateral decubitus)
39329-8|Shoulder - bilateral X-ray AP (W internal rotation and W external rotation)
39328-0|Shoulder - left X-ray AP (W internal rotation and W external rotation)
39395-9|Shoulder - right X-ray AP (W internal rotation and W external rotation)
39321-5|Shoulder X-ray AP (W internal rotation and W external rotation) and axillary
39336-3|Shoulder - bilateral X-ray AP (W internal rotation and W external rotation) and axillary
39335-5|Shoulder - left X-ray AP (W internal rotation and W external rotation) and axillary
39337-1|Shoulder - bilateral X-ray AP (W internal rotation and W external rotation) and axillary and outlet
39344-7|Shoulder - bilateral X-ray AP (W internal rotation and W external rotation) and axillary and Y
39338-9|Shoulder - left X-ray AP (W internal rotation and W external rotation) and axillary and Y
39397-5|Shoulder - right X-ray AP (W internal rotation and W external rotation) and West Point
39343-9|Shoulder - bilateral X-ray AP (W internal rotation and W external rotation) and Y
39348-8|Shoulder - left X-ray AP (W internal rotation and W external rotation) and Y
39325-6|Shoulder - left X-ray AP (W internal rotation) and Grashey and axillary and outlet
39346-2|Shoulder - bilateral X-ray AP (W internal rotation) and West Point
39347-0|Shoulder - left X-ray AP (W internal rotation) and West Point
39396-7|Shoulder - right X-ray AP (W internal rotation) and West Point
24632-2|Chest X-ray AP portable
37075-9|Hip X-ray AP portable
43561-0|Chest and Abdomen X-ray AP upright and AP chest
38003-0|Foot - left X-ray AP standing
38815-7|Foot - right X-ray AP standing
42406-9|Spine Lumbar X-ray AP W and WO left bending
42407-7|Spine Lumbar X-ray AP W and WO right bending
42445-7|Spine Thoracic X-ray AP W left bending and WO bending
37484-3|Knee - left X-ray AP W manual stress
37746-5|Knee - right X-ray AP W manual stress
42403-6|Spine Lumbar X-ray AP W right bending and W left bending
42408-5|Spine Lumbar X-ray AP W right bending and W left bending and WO bending
42444-0|Spine Thoracic X-ray AP W right bending and W left bending and WO bending
42446-5|Spine Thoracic X-ray AP W right bending and WO bending
39403-1|Shoulder X-ray axillary and transcapular
37127-8|Shoulder - bilateral X-ray axillary and Y
37128-6|Shoulder - left X-ray axillary and Y
37807-5|Shoulder - right X-ray axillary and Y
46386-9|Teeth X-ray bitewing
39884-2|Bone Scan blood pool
39861-0|Heart Scan blood pool
42709-6|Liver Scan blood pool
39860-2|Heart Scan blood pool W stress and W radionuclide IV
26352-5|Wrist - bilateral and Hand - bilateral X-ray bone age
26353-3|Wrist - left and Hand - left X-ray bone age
26354-1|Wrist - right and Hand - right X-ray bone age
24724-7|Wrist and Hand X-ray bone age
37362-1|Bones X-ray bone age
24591-0|Brain Scan brain death protocol W Tc-99m HMPAO IV
37996-6|Calcaneus X-ray Broden
37995-8|Calcaneus - bilateral X-ray Broden
37997-4|Calcaneus - left X-ray Broden
38814-0|Calcaneus - right X-ray Broden
37486-8|Ankle X-ray Broden W manual stress
37852-1|Sinuses X-ray Caldwell and Waters
39859-4|Brain Scan delayed static
39875-0|Scan delayed W GA-67 IV
39840-4|Scan delayed W I-131 MIBG IV
39842-0|Scan delayed W In-111 Satumomab IV
39874-3|Head Cistern Scan delayed W radionuclide IT
39819-8|Bone Scan delayed
39741-4|Parathyroid Scan delayed
24605-8|Breast Mammogram diagnostic
39152-4|Breast FFD mammogram diagnostic
69158-4|Breast implant X-ray diagnostic
48475-8|Breast implant - bilateral Mammogram diagnostic
69150-1|Breast implant - left Mammogram diagnostic
69259-0|Breast implant - right Mammogram diagnostic
26346-7|Breast - bilateral Mammogram diagnostic
39154-0|Breast - bilateral FFD mammogram diagnostic
26347-5|Breast - left Mammogram diagnostic
42169-3|Breast - left FFD mammogram diagnostic
26348-3|Breast - right Mammogram diagnostic
42168-5|Breast - right FFD mammogram diagnostic
46350-5|Breast - unilateral Mammogram diagnostic
24604-1|Breast Mammogram diagnostic limited
26349-1|Breast - bilateral Mammogram diagnostic limited
26350-9|Breast - left Mammogram diagnostic limited
26351-7|Breast - right Mammogram diagnostic limited
46351-3|Breast implant - bilateral Mammogram displacement
39895-8|Gallbladder Scan ejection fraction W Tc-99m DISIDA IV
39887-5|Heart Scan first pass and ejection fraction at rest and W radionuclide IV
39889-1|Heart Scan first pass and ejection fraction
39885-9|Heart Scan first pass and ventricular volume
39910-5|Heart Scan first pass and wall motion and ejection fraction
39912-1|Heart Scan first pass and wall motion and ventricular volume and ejection fraction
39909-7|Heart Scan first pass and wall motion and ventricular volume and ejection fraction W stress and W radionuclide IV
39908-9|Heart Scan first pass and wall motion and ventricular volume W stress and W radionuclide IV
39886-7|Heart Scan first pass and wall motion at rest and W radionuclide IV
39890-9|Heart Scan first pass and wall motion
39888-3|Heart Scan first pass and wall motion W stress and W radionuclide IV
39867-7|Heart Scan first pass at rest and W radionuclide IV
39863-6|Heart Scan first pass at rest and W stress and W radionuclide IV
39866-9|Heart Scan first pass at rest and W Tc-99m Sestamibi IV
39864-4|Heart Scan first pass
39865-1|Left ventricle Scan first pass
39869-3|Heart Scan first pass W stress and W radionuclide IV
39868-5|Heart Scan first pass W stress and W Tc-99m Sestamibi IV
39893-3|Heart Scan flow for shunt detection
43644-4|Brain Scan flow limited
39858-6|Bone Scan flow
39636-6|Brain Scan flow
39871-9|Heart Scan flow
42261-8|Kidney - bilateral Scan flow
42262-6|Liver Scan flow
43653-5|Liver and Spleen Scan flow
39847-9|Parotid gland Scan flow
39899-0|Salivary gland Scan flow
42308-7|Scrotum and Testicle Scan flow
42263-4|Spleen Scan flow
39856-0|Thyroid Scan flow
43500-8|Vessel Scan flow
44148-5|Brain Scan flow W Tc-99m bicisate IV
43642-8|Brain Scan flow W Tc-99m DTPA IV
43664-2|Renal vessels Scan flow W Tc-99m DTPA IV
43643-6|Brain Scan flow W Tc-99m glucoheptonate IV
43666-7|Kidney - bilateral and Renal vessels Scan flow W Tc-99m glucoheptonate IV
43663-4|Renal vessels Scan flow W Tc-99m glucoheptonate IV
43665-9|Renal vessels Scan flow W Tc-99m Mertiatide IV
39870-1|Heart Scan flow W Tc-99m pertechnetate IV
43654-3|Liver Scan flow W Tc-99m tagged RBC IV
39685-3|Scan for abscess W GA-67 IV
39940-2|Lung Scan Clearance W Tc-99m DTPA aerosol inhaled
43787-1|Skull and Facial bones and Mandible X-ray for dental measurement
43648-5|Scan for endocrine tumor multiple areas W I-131 MIBG IV
43649-3|Scan for endocrine tumor multiple areas W In-111 pentetreotide IV
39827-1|Scan for endocrine tumor whole body W I-131 MIBG IV
39828-9|Scan for endocrine tumor whole body W In-111 pentetreotide IV
39327-2|Abdomen and Fetus X-ray for fetal age
44208-7|Orbit X-ray for foreign body
30720-7|Orbit - bilateral X-ray for foreign body
42311-1|Orbit - left X-ray for foreign body
42312-9|Orbit - right X-ray for foreign body
39768-7|Stomach Scan for gastric emptying W Tc-99m SC PO
39767-9|Stomach Scan for gastric emptying liquid phase W radionuclide PO
24997-9|Stomach Scan for gastric emptying solid phase W Tc-99m SC PO
39769-5|Stomach Scan for gastric emptying W radionuclide PO
39892-5|Heart Scan for infarct and first pass
39891-7|Heart Scan for infarct and first pass W Tc-99m PYP IV
43646-9|Heart Scan for infarct qualitative and quantitative
43645-1|Heart Scan for infarct qualitative
43647-7|Heart Scan for infarct quantitative
39653-1|Heart Scan for infarct
39657-2|Heart Scan for infarct W Tc-99m PYP IV
39933-7|Scan for infection multiple areas W GA-67 IV
39830-5|Scan for infection whole body W GA-67 IV
39677-0|Scan for infection W GA-67 IV
39490-8|Femur - right and Tibia - right X-ray for leg length
24700-7|Femur and Tibia X-ray for leg length
39686-1|Scan for lymphoma W GA-67 IV
42170-1|Scan for lymphoma
39672-1|Esophagus Scan for motility W radionuclide PO
72256-1|Abdomen X-ray for motility with radioopaque markers
24571-2|Biliary ducts and Gallbladder Scan for patency of biliary structures and ejection fraction W sincalide and W radionuclide IV
24572-0|Biliary ducts and Gallbladder Scan for patency of biliary structures W Tc-99m IV
43788-9|Tube Fluoroscopy for patency W contrast via tube
43789-7|Liver and Biliary ducts and Gallbladder Scan for patency W Tc-99m IV
39673-9|Esophagus Scan for reflux W radionuclide PO
30650-6|Unspecified body region Fluoroscopy for shunt
39665-5|Heart Scan for shunt detection
39664-8|Heart Scan for shunt detection W Tc-99m MAA IV
39848-7|Peritoneovenous shunt Scan for patency W In-111 IT
39849-5|Peritoneovenous shunt Scan for patency W radionuclide IT
24876-5|Peritoneovenous shunt Scan for patency W Tc-99m DTPA IT
44149-3|Peritoneovenous shunt Scan for patency W Tc-99m MAA inj
39954-3|Vein Scan for thrombosis
44140-2|Abdomen and Pelvis Scan for tumor
39831-3|Scan for tumor limited W GA-67 IV
39951-9|Scan for tumor multiple area W Tc-99m Sestamibi IV
39934-5|Scan for tumor multiple areas W GA-67 IV
39829-7|Scan for tumor whole body W GA-67 IV
42171-9|Scan for tumor whole body
39749-7|Scan for tumor whole body W Tc-99m Sestamibi IV
39679-6|Scan for tumor W GA-67 IV
39750-5|Scan for tumor W Tc-99m Sestamibi IV
42305-3|Scan for tumor W Tl-201 IV
42397-0|Chest X-ray frontal stereo
39923-8|Heart Scan gated and ejection fraction at rest and W radionuclide IV
39917-0|Heart Scan gated and ejection fraction
39919-6|Heart Scan gated and first pass
39925-3|Heart Scan gated and wall motion and ejection fraction at rest and W radionuclide IV
39931-1|Heart Scan gated and wall motion and ejection fraction
42306-1|Heart Scan gated and wall motion
39929-5|Heart Scan gated and wall motion W stress and W radionuclide IV
39921-2|Heart Scan gated at rest and W radionuclide IV
39924-6|Heart Scan gated at rest and W stress and W radionuclide IV
39922-0|Heart Scan gated at rest and W Tc-99m pertechnetate IV
39920-4|Heart Scan gated at rest and W Tc-99m Sestamibi IV
39915-4|Heart Scan gated
39928-7|Heart Scan gated W stress and W radionuclide IV
39927-9|Heart Scan gated W stress and W Tc-99m pertechnetate IV
39914-7|Heart Scan gated W Tc-99m Sestamibi IV
46348-9|Chest X-ray GE 2 and PA and Lateral views
44210-3|Ankle X-ray GE 3 views
48480-8|Ankle - bilateral X-ray GE 3 views
46390-1|Ankle - left X-ray GE 3 views
46347-1|Ankle - right X-ray GE 3 views
48481-6|Elbow - bilateral X-ray GE 3 views
46344-8|Elbow - left X-ray GE 3 views
46345-5|Elbow - right X-ray GE 3 views
48479-0|Facial bones X-ray GE 3 views
43492-8|Finger fifth - left X-ray GE 3 views
43497-7|Finger fifth - right X-ray GE 3 views
43491-0|Finger fourth - left X-ray GE 3 views
43496-9|Finger fourth - right X-ray GE 3 views
43489-4|Finger second - left X-ray GE 3 views
43494-4|Finger second - right X-ray GE 3 views
43490-2|Finger third - left X-ray GE 3 views
43495-1|Finger third - right X-ray GE 3 views
44188-1|Foot X-ray GE 3 views
48478-2|Foot - bilateral X-ray GE 3 views
48477-4|Foot - left X-ray GE 3 views
48476-6|Foot - right X-ray GE 3 views
47370-2|Hand - left X-ray GE 3 views
47371-0|Hand - right X-ray GE 3 views
43498-5|Knee - left X-ray GE 3 views
43482-9|Knee - right X-ray GE 3 views
47381-9|Mastoid X-ray GE 3 views
43543-8|Pelvis X-ray GE 3 views
44189-9|Sacroiliac Joint X-ray GE 3 views
48746-2|Sacroiliac joint - bilateral X-ray GE 3 views
43486-0|Sinuses X-ray GE 3 views
46377-8|Skull X-ray GE 3 views
48482-4|Sternoclavicular Joints X-ray GE 3 views
43488-6|Thumb - left X-ray GE 3 views
43493-6|Thumb - right X-ray GE 3 views
44190-7|Wrist X-ray GE 3 views
48483-2|Wrist - bilateral X-ray GE 3 views
46346-3|Wrist - left X-ray GE 3 views
46343-0|Wrist - right X-ray GE 3 views
48485-7|Ribs - bilateral and Chest X-ray GE 3 and PA Chest views
48486-5|Ribs - left and Chest X-ray GE 3 and PA Chest views
48484-0|Ribs - right and Chest X-ray GE 3 and PA Chest views
44191-5|Ribs and Chest X-ray GE 3 and PA Chest views
44239-2|Ribs - unilateral and Chest X-ray Ge 3 and PA Chest Portable views
44193-1|Hand X-ray GE 3 Portable views
44192-3|Pelvis X-ray GE 3 Portable views
44211-1|Chest X-ray GE 4 views
47367-8|Chest Fluoroscopy GE 4 views
47374-4|Knee - left X-ray GE 4 views
47376-9|Knee - right X-ray GE 4 views
47379-3|Mandible X-ray GE 4 views
48747-0|Orbit - bilateral X-ray GE 4 views
48487-3|Skull X-ray GE 4 views
44212-9|Spine Cervical X-ray GE 4 views
47382-7|Spine Lumbar X-ray GE 4 views
47368-6|Chest X-ray GE 4 and Pa and Lateral views
44194-9|Spine X-ray GE 4 views W right bending and W left bending
44195-6|Knee X-ray GE 5 views
43524-8|Skull X-ray GE 5 views
44197-2|Knee - bilateral X-ray GE 5 views standing
44196-4|Spine Lumbar X-ray GE 5 views W right bending and W left bending
49570-5|Ankle - bilateral X-ray GE 6 views
37160-9|Shoulder - left X-ray Grashey and axillary
38793-6|Shoulder - right X-ray Grashey and axillary
37158-3|Shoulder - left X-ray Grashey and axillary and outlet
37806-7|Shoulder - right X-ray Grashey and axillary and outlet
37161-7|Shoulder - bilateral X-ray Grashey and axillary and outlet and Zanca
69267-3|Shoulder X-ray Grashey and axillary and Y
37538-6|Shoulder - left X-ray Grashey and axillary and Y
38789-4|Shoulder - right X-ray Grashey and axillary and Y
37157-5|Shoulder - left X-ray Grashey and outlet
38791-0|Shoulder - right X-ray Grashey and outlet
39350-4|Shoulder - bilateral X-ray Grashey and outlet and Serendipity
37162-5|Shoulder - left X-ray Grashey and outlet and Serendipity
38794-4|Shoulder - right X-ray Grashey and outlet and Serendipity
37167-4|Shoulder - left X-ray Grashey and West Point
38795-1|Shoulder - right X-ray Grashey and West Point
69156-8|Shoulder - left X-ray Grashey and Y
43790-5|Shoulder - right X-ray Grashey and Y
38004-8|Shoulder - left X-ray Grashey W and WO weight
38816-5|Shoulder - right X-ray Grashey W and WO weight
37539-4|Breast Mammogram grid
37540-2|Knee - bilateral X-ray Holmblad standing
30771-0|Pelvis X-ray inlet and outlet
37627-7|Pelvis X-ray inlet and outlet and oblique
37164-1|Facial bones X-ray lateral and Caldwell and Waters
37864-6|Sinuses X-ray lateral and Caldwell and Waters
37165-8|Facial bones X-ray lateral and Caldwell and Waters and submentovertex
37166-6|Facial bones X-ray lateral and Caldwell and Waters and submentovertex and Towne
37871-1|Skull X-ray lateral and Caldwell and Waters and Towne
37134-4|Ankle - bilateral X-ray lateral and Mortise
37135-1|Ankle - left X-ray lateral and Mortise
37670-7|Ankle - right X-ray lateral and Mortise
42382-2|Ankle - left X-ray lateral and Mortise and Broden W manual stress
39366-0|Scapula X-ray lateral and outlet
43464-7|Ribs - bilateral and Chest X-ray lateral and PA chest
37603-8|Ribs - left and Chest X-ray lateral and PA chest
39100-3|Ribs - right and Chest X-ray lateral and PA chest
39101-1|Ribs and Chest X-ray lateral and PA chest
39341-3|Chest X-ray lateral and PA W inspiration and expiration
39406-4|Sternum X-ray lateral and right anterior oblique
39405-6|Sternum X-ray lateral and right oblique and left oblique
42436-6|Sella turcica X-ray lateral and Towne
37869-5|Skull X-ray lateral and Towne
37605-3|Nasal bones X-ray lateral and Waters
37862-0|Sinuses X-ray lateral and Waters
37136-9|Shoulder - left X-ray lateral and Y
37803-4|Shoulder - right X-ray lateral and Y
39340-5|Spine Lumbar X-ray lateral standing and W flexion and W extension
37133-6|Spine Cervical X-ray lateral W flexion and W extension
37132-8|Spine Lumbar X-ray lateral W flexion and W extension
38010-5|Spine Thoracic X-ray lateral W flexion and W extension
37929-7|Wrist X-ray lateral W flexion and W extension
69157-6|Wrist - left X-ray lateral W flexion and W extension
39515-2|Wrist - right X-ray lateral W flexion and W extension
37474-4|Ankle - left X-ray lateral W manual stress
37669-9|Ankle - right X-ray lateral W manual stress
43480-3|Joint X-ray lateral W manual stress
37541-0|Mastoid - bilateral X-ray law and Mayer and Stenver and Towne
47380-1|Mandible X-ray LE 3 views
43470-4|Skull X-ray LE 3 views
47377-7|Knee - right X-ray LE 4 views
24610-8|Breast Mammogram limited
26287-3|Breast - bilateral Mammogram limited
26289-9|Breast - left Mammogram limited
26291-5|Breast - right Mammogram limited
41826-9|Elbow - left X-ray limited
41785-7|Elbow - right X-ray limited
36737-5|Facial bones X-ray limited
41830-1|Hand - left X-ray limited
41789-9|Hand - right X-ray limited
36738-3|Mandible X-ray limited
36893-6|Mastoid X-ray limited
42007-5|Mastoid - bilateral X-ray limited
37646-7|Sacroiliac Joint X-ray limited
44209-5|Sinuses X-ray limited
48466-7|Skull X-ray limited
42710-4|Spine Cervical X-ray limited
36739-1|Wrist - bilateral X-ray limited
38838-9|Wrist - left X-ray limited
37642-6|Wrist - right X-ray limited
41797-2|Colon Fluoroscopy limited W air and barium contrast PR
42335-0|Spine Cervical Fluoroscopy limited W contrast IT
38125-1|Spine Cervical and Thoracic and Lumbar Fluoroscopy limited W contrast IT
38120-2|Spine Thoracic Fluoroscopy limited W contrast IT
37137-7|Kidney X-ray limited W contrast IV
39687-9|Scan limited W GA-67 IV
39754-7|Thyroid Scan limited W I-131 IV
49571-3|Scan limited W I-131 MIBG IV
39843-8|Scan limited W In-111 Satumomab IV
41836-8|Bone Scan limited W In-111 tagged WBC IV
39627-5|Bone Scan limited
39822-2|Bone marrow Scan limited
39645-7|Breast Scan limited
39695-2|Lung Scan limited
39936-0|Joint Scan limited
37542-8|Breast Mammogram magnification
37543-6|Breast - bilateral Mammogram magnification
37554-3|Breast - bilateral Mammogram magnification and spot
38854-6|Breast - left Mammogram magnification and spot
37769-7|Breast - right Mammogram magnification and spot
30769-4|Pelvis and Hip - bilateral X-ray max abduction
38086-5|Knee X-ray Merchants 30 and 45 and 60 degrees
39935-2|Scan multiple areas W GA-67 IV
39949-3|Scan multiple areas W In-111 Satumomab IV
39904-8|Bone Scan multiple areas
39907-1|Bone marrow Scan multiple areas
39937-8|Joint Scan multiple areas
39950-1|Prostate Scan multiple areas W Tc-99m capromab pendatide IV
36608-8|Elbow X-ray oblique
36740-9|Elbow - bilateral X-ray oblique
36741-7|Elbow - left X-ray oblique
37687-1|Elbow - right X-ray oblique
36744-1|Humerus - left X-ray oblique
37737-4|Humerus - right X-ray oblique
36619-5|Knee X-ray oblique
36745-8|Knee - bilateral X-ray oblique
36746-6|Knee - left X-ray oblique
37757-2|Knee - right X-ray oblique
36747-4|Mandible X-ray oblique
37630-1|Pelvis X-ray oblique
36742-5|Radius - bilateral and Ulna - bilateral X-ray oblique
36743-3|Radius - left and Ulna.left X-ray oblique
37709-3|Radius - right and Ulna - right X-ray oblique
36748-2|Spine Cervical X-ray oblique
43791-3|Spine Lumbar X-ray oblique
48749-6|Spine Thoracic X-ray oblique
36749-0|Tibia - left and Fibula - left X-ray oblique
37817-4|Tibia - right and Fibula - right X-ray oblique
36894-4|Tibia and Fibula X-ray oblique
37544-4|Wrist - bilateral X-ray oblique
38839-7|Wrist - left X-ray oblique
37643-4|Wrist - right X-ray oblique
42398-8|Foot X-ray oblique and (AP and lateral) standing
37139-3|Spine Cervical X-ray oblique and lateral W flexion and W extension
37154-2|Knee X-ray oblique and Sunrise
37155-9|Knee X-ray oblique and Sunrise and tunnel
43469-6|Unspecified body region X-ray of foreign body
37063-5|Unspecified body region Fluoroscopy of foreign body
37546-9|Temporomandibular joint - bilateral X-ray open and closed mouth
48491-5|Temporomandibular joint - left X-ray open and closed mouth
48490-7|Temporomandibular joint - right X-ray open and closed mouth
48699-3|Temporomandibular Joint - unilateral X-ray open and closed mouth
37152-6|Shoulder - bilateral X-ray outlet and Y
37140-1|Shoulder - left X-ray outlet and Y
37804-2|Shoulder - right X-ray outlet and Y
36750-8|Chest X-ray PA and AP lateral-decubitus
42272-5|Chest X-ray PA and lateral
36751-6|Chest Fluoroscopy PA and lateral
36752-4|Hand - bilateral X-ray PA and lateral
36753-2|Hand - left X-ray PA and lateral
37713-5|Hand - right X-ray PA and lateral
36754-0|Mandible X-ray PA and lateral
30721-5|Sinuses X-ray PA and lateral
37547-7|Wrist - bilateral X-ray PA and lateral
37548-5|Wrist - left X-ray PA and lateral
37835-6|Wrist - right X-ray PA and lateral
37143-5|Chest X-ray PA and lateral and AP lateral-decubitus
37144-3|Chest X-ray PA and lateral and AP left lateral-decubitus
37145-0|Chest X-ray PA and lateral and AP right lateral-decubitus
37142-7|Hand - bilateral X-ray PA and lateral and Ball Catcher
37860-4|Sinuses X-ray PA and lateral and Caldwell and Waters
37146-8|Chest X-ray PA and lateral and left oblique
30741-3|Chest X-ray PA and lateral and lordotic upright
39078-1|Finger X-ray PA and lateral and oblique
36755-7|Hand X-ray PA and lateral and oblique
36756-5|Hand - bilateral X-ray PA and lateral and oblique
36757-3|Hand - left X-ray PA and lateral and oblique
37715-0|Hand - right X-ray PA and lateral and oblique
37884-4|Sternum X-ray PA and lateral and oblique
37549-3|Wrist - bilateral X-ray PA and lateral and oblique
37550-1|Wrist - left X-ray PA and lateral and oblique
37836-4|Wrist - right X-ray PA and lateral and oblique
36758-1|Chest X-ray PA and lateral and oblique and lordotic
37148-4|Mandible X-ray PA and lateral and oblique and Towne
37147-6|Chest X-ray PA and lateral and right oblique
30742-1|Chest X-ray PA and lateral and right oblique and left oblique
30743-9|Chest X-ray PA and lateral and right oblique and left oblique portable
30744-7|Chest X-ray PA and lateral and right or-left oblique
24643-9|Chest X-ray PA and lateral and right or-left oblique upright
37149-2|Patella - left X-ray PA and lateral and Sunrise
38790-2|Patella - right X-ray PA and lateral and Sunrise
37859-6|Sinuses X-ray PA and lateral and Waters
69271-5|Skull X-ray PA and lateral and Waters and Towne
24647-0|Chest X-ray PA and lateral upright
24644-7|Chest X-ray PA and lateral upright portable
36759-9|Chest X-ray PA and lordotic
39079-9|Hand X-ray PA and oblique
37141-9|Chest X-ray PA and right lateral
39519-4|Skull X-ray PA and right lateral and left lateral
39521-0|Skull X-ray PA and right lateral and left lateral and Caldwell and Towne
39520-2|Skull X-ray PA and right lateral and left lateral and Towne
24646-2|Chest X-ray PA and right lateral and right oblique and left oblique upright
24645-4|Chest X-ray PA and right lateral and right oblique and left oblique upright portable
37150-0|Chest X-ray PA and right oblique and left oblique
24635-5|Chest X-ray PA upright W inspiration and expiration
46378-6|Knee - bilateral X-ray PA standing and W flexion
43660-0|Heart Scan perfusion qualitative at rest and W radionuclide IV
43661-8|Heart Scan perfusion quantitative at rest and W radionuclide IV
43658-4|Heart Scan perfusion quantitative
43656-8|Lung Scan perfusion quantitative
39719-0|Heart Scan perfusion at rest and W adenosine and W radionuclide IV
43777-2|Heart Scan perfusion at rest and W adenosine and W Tl-201 IV
39722-4|Heart Scan perfusion at rest and W dipyridamole and W radionuclide IV
39720-8|Heart Scan perfusion at rest and W dipyridamole and W Tc-99m Sestamibi IV
39728-1|Heart Scan perfusion at rest and W radionuclide IV
39726-5|Heart Scan perfusion at rest and W stress and W radionuclide IV
39727-3|Heart Scan perfusion at rest and W stress and W Tc-99m Sestamibi IV
39699-4|Heart Scan perfusion at rest and W Tc-99m Sestamibi IV
39701-8|Heart Scan perfusion W adenosine and W radionuclide IV
39731-5|Heart Scan perfusion W adenosine and W Tc-99m Sestamibi IV
39735-6|Heart Scan perfusion W adenosine and W Tl-201 IV
39708-3|Heart Scan perfusion W dipyridamole and W radionuclide IV
39709-1|Heart Scan perfusion W dipyridamole and W Tc-99m IV
39705-9|Heart Scan perfusion W dipyridamole and W Tc-99m Sestamibi IV
39707-5|Heart Scan perfusion W dipyridamole and W Tl-201 IV
39703-4|Heart Scan perfusion W dobutamine and W radionuclide IV
39702-6|Heart Scan perfusion W dobutamine and W Tc-99m Sestamibi IV
39733-1|Heart Scan perfusion W dobutamine and W Tl-201 IV
39941-0|Lung Scan perfusion W particulate radionuclide IV
39833-9|Lung Scan perfusion W radionuclide gaseous inhaled
39716-6|Heart Scan perfusion
39697-8|Lung Scan perfusion
39730-7|Heart Scan perfusion W stress and W radionuclide IV
39732-3|Heart Scan perfusion W stress and W Tc-99m Sestamibi IV
39715-8|Heart Scan perfusion W stress and W Tl-201 IV
39704-2|Heart Scan perfusion W Tc-99m Sestamibi IV
39714-1|Heart Scan perfusion W Tl-201 IV
39713-3|Heart Scan perfusion W Tl-201 IV and Tc-99m Tetrofosmin IV
30765-2|Acetabulum X-ray portable
30764-5|Acetabulum - bilateral X-ray portable
41823-6|Ankle - left X-ray portable
41782-4|Ankle - right X-ray portable
30746-2|Chest X-ray portable
41827-7|Elbow - left X-ray portable
41786-5|Elbow - right X-ray portable
41773-3|Facial bones X-ray portable
41818-6|Femur - left X-ray portable
41778-2|Femur - right X-ray portable
43570-1|Hand X-ray portable
41829-3|Hand - left X-ray portable
41788-1|Hand - right X-ray portable
37168-2|Hip X-ray portable
37169-0|Hip - left X-ray portable
38796-9|Hip - right X-ray portable
37170-8|Humerus X-ray portable
41825-1|Humerus - left X-ray portable
41784-0|Humerus - right X-ray portable
41820-2|Knee - left X-ray portable
41779-0|Knee - right X-ray portable
30792-6|Patella X-ray portable
30772-8|Pelvis X-ray portable
30747-0|Ribs X-ray portable
41831-9|Ribs - left X-ray portable
41791-5|Ribs - right X-ray portable
46391-9|Shoulder X-ray portable
41824-4|Shoulder - left X-ray portable
41783-2|Shoulder - right X-ray portable
30723-1|Skull X-ray portable
37171-6|Spine Cervical X-ray portable
44203-8|Spine Cervical and Thoracic and Lumbar X-ray portable
37172-4|Spine Lumbar X-ray portable
41828-5|Wrist - left X-ray portable
41787-3|Wrist - right X-ray portable
37151-8|Unspecified body region Fluoroscopy portable
30731-4|Zygomatic arch X-ray portable
30730-6|Zygomatic arch - bilateral X-ray portable
24634-8|Chest X-ray portable W inspiration and expiration
24824-5|Lung Scan portable
42402-8|Unspecified body region X-ray post mortem
43657-6|Lung Scan quantitative
30733-0|Chest X-ray right and left oblique portable
37131-0|Abdomen X-ray right lateral and left lateral
37138-5|Abdomen X-ray right oblique and left oblique
41792-3|Chest X-ray right oblique and left oblique
24651-2|Chest X-ray right oblique and left oblique upright
42414-3|Chest X-ray right oblique and left oblique W nipple markers
37016-3|Breast - bilateral Mammogram roll
37017-1|Breast - left Mammogram roll
37775-4|Breast - right Mammogram roll
30740-5|Chest X-ray right or-left oblique
30739-7|Chest X-ray right or-left oblique portable
43479-5|Aorta abdominal Fluoroscopic angiogram runoff W contrast IA
30838-7|Aorta and Femoral artery - bilateral Fluoroscopic angiogram runoff W contrast IA
37364-7|Aorta and Femoral artery - left Fluoroscopic angiogram runoff W contrast IA
38799-3|Aorta and Femoral artery - right Fluoroscopic angiogram runoff W contrast IA
38107-9|Wrist X-ray scaphoid
37304-3|Wrist - bilateral X-ray scaphoid
37302-7|Wrist - left X-ray scaphoid
38115-2|Wrist - right X-ray scaphoid
24930-0|Spine Thoracic and Lumbar X-ray scoliosis
30715-7|Spine Thoracic and Lumbar X-ray scoliosis AP and lateral
42424-2|Spine Thoracic and Lumbar X-ray scoliosis AP and lateral sitting
39367-8|Spine Thoracic and Lumbar X-ray scoliosis AP and lateral standing
42472-1|Spine Thoracic and Lumbar X-ray scoliosis AP in traction
42425-9|Spine Thoracic and Lumbar X-ray scoliosis AP standing and W right bending and W left bending and WO bending
43569-3|Spine Thoracic and Lumbar X-ray scoliosis AP upright and supine
30716-5|Spine Thoracic and Lumbar X-ray scoliosis lateral
30717-3|Spine Thoracic and Lumbar X-ray scoliosis standing
24929-2|Spine Thoracic and Lumbar X-ray scoliosis W flexion and W extension
24606-6|Breast Mammogram screening
39153-2|Breast FFD mammogram screening
69159-2|Breast implant X-ray screening
48492-3|Breast implant - bilateral Mammogram screening
26175-0|Breast - bilateral Mammogram screening
42174-3|Breast - bilateral FFD mammogram screening
26176-8|Breast - left Mammogram screening
46355-4|Breast - left FFD mammogram screening
26177-6|Breast - right Mammogram screening
46354-7|Breast - right FFD mammogram screening
46356-2|Breast - unilateral Mammogram screening
37022-1|Calcaneus X-ray ski jump
37021-3|Calcaneus - bilateral X-ray ski jump
37023-9|Calcaneus - left X-ray ski jump
38778-7|Calcaneus - right X-ray ski jump
37551-9|Breast Mammogram spot
37552-7|Breast - bilateral Mammogram spot
38807-4|Breast - right Mammogram spot
37553-5|Breast - left Mammogram spot compression
43550-3|Brain Scan static and flow
39952-7|Scrotum and Testicle Scan static and flow
39676-2|Scan static for infection W GA-67 IV
39894-1|Heart Scan static for shunt detection
39896-6|Scan static for tumor W GA-67 IV
39814-9|Bone Scan static limited
39634-1|Brain Scan static limited
39903-0|Bone Scan static multiple areas
39817-2|Bone Scan static whole body
39815-6|Bone Scan static
39824-8|Bone marrow Scan static
39633-3|Brain Scan static
39853-7|Kidney - bilateral Scan static
39832-1|Liver Scan static
39878-4|Liver and Spleen Scan static
39900-6|Salivary gland Scan static
39855-2|Scrotum and Testicle Scan static
43501-6|Vessel Scan static
44150-1|Brain Scan static W Tc-99m bicisate IV
39854-5|Kidney - bilateral Scan static W Tc-99m DMSA IV
37153-4|Mastoid X-ray Stenver and Arcelin
69136-0|Knee X-ray Sunrise and tunnel
37163-3|Knee - bilateral X-ray Sunrise and tunnel
37156-7|Knee - left X-ray Sunrise and tunnel
37759-8|Knee - right X-ray Sunrise and tunnel
39345-4|Knee - left X-ray Sunrise and tunnel standing
69255-8|Knee - right X-ray Sunrise and tunnel standing
38088-1|Knee - bilateral X-ray Sunrise 20 and 40 and 60 degrees
38087-3|Knee - left X-ray Sunrise 20 and 40 and 60 degrees
38824-9|Knee - right X-ray Sunrise 20 and 40 and 60 degrees
24579-5|Bones long X-ray survey
43518-0|Bones X-ray survey
37365-4|Bones X-ray survey for metastasis
39518-6|Bones long X-ray survey limited
43519-8|Bones X-ray survey limited
38089-9|Bones X-ray survey limited for metastasis
37159-1|Foot - left X-ray tarsal
38792-8|Foot - right X-ray tarsal
43796-2|Wrist - bilateral X-ray tunnel.carpal
69304-4|Wrist X-ray ulnar deviation
69303-6|Wrist X-ray ulnar deviation and radial deviation
69072-7|Wrist - bilateral X-ray ulnar deviation and radial deviation
37555-0|Wrist - left X-ray ulnar deviation and radial deviation
38808-2|Wrist - right X-ray ulnar deviation and radial deviation
43532-1|Chest and Abdomen X-ray upright and PA chest
39944-4|Lung Scan ventilation and equilibrium and washout W radionuclide inhaled
39948-5|Lung Scan ventilation and equilibrium and washout W radionuclide inhaled single breath
39947-7|Lung Scan ventilation and equilibrium W radionuclide inhaled single breath
39946-9|Lung Scan ventilation and perfusion and differential W radionuclide inhaled and W radionuclide IV
39943-6|Lung Scan ventilation and perfusion W radionuclide inhaled and W particulate radionuclide IV
30697-7|Pulmonary system Scan ventilation and perfusion W radionuclide inhaled and W radionuclide IV
39942-8|Lung Scan ventilation and perfusion W radionuclide inhaled single breath and W particulate radionuclide IV
24888-0|Pulmonary system Scan ventilation and perfusion W Xe-133 inhaled and W Tc-99m MAA IV
39835-4|Lung Scan ventilation W radionuclide aerosol inhaled
39836-2|Lung Scan ventilation W radionuclide gaseous inhaled
39945-1|Lung Scan ventilation W radionuclide gaseous inhaled single breath
39837-0|Lung Scan ventilation W radionuclide inhaled
39834-7|Lung Scan ventilation W Tc-99m DTPA aerosol inhaled
46361-2|Lung Scan ventilation W Xe-133 inhaled
39932-9|Heart Scan wall motion and ejection fraction
39873-5|Heart Scan wall motion
39683-8|Scan whole body W GA-67 IV
39698-6|Scan whole body W I-131 MIBG IV
39845-3|Scan whole body W In-111 Satumomab IV
42711-2|Scan whole body W In-111 tagged WBC IV
42175-0|Scan whole body
39818-0|Bone Scan whole body
39826-3|Bone marrow Scan whole body
39669-7|Scan whole body W Tc-99m Arcitumomab IV
24713-0|Gallbladder X-ray 48 hours post contrast PO
39660-6|Heart Scan at rest and W dipyridamole and W radionuclide IV
39661-4|Heart Scan at rest and W dobutamine and W radionuclide IV
39663-0|Heart Scan at rest and W stress and W radionuclide IV
42309-5|Heart Scan at rest and W stress and W Tl-201 IV
24750-2|Heart Scan at rest and W Tl-201 IV
43459-7|Brain Scan during electroconvulsive shock treatment
24577-9|Bone X-ray during surgery
47372-8|Hip X-ray during surgery
25070-4|Unspecified body region Fluoroscopy during surgery
24574-6|Biliary ducts and Gallbladder Fluoroscopy during surgery W contrast biliary duct
46352-1|Breast duct Mammogram during surgery W contrast intra duct
43485-2|Kidney X-ray during surgery W contrast retrograde
39150-8|Breast FFD mammogram Post Localization
69251-7|Breast Mammogram Post Wire Placement
42415-0|Breast - bilateral Mammogram Post Wire Placement
42416-8|Breast - left Mammogram Post Wire Placement
37201-1|Ankle X-ray standing
37202-9|Ankle - bilateral X-ray standing
37203-7|Ankle - left X-ray standing
37676-4|Ankle - right X-ray standing
37205-2|Calcaneus X-ray standing
37206-0|Calcaneus - left X-ray standing
37720-0|Calcaneus - right X-ray standing
38845-4|Femur - left X-ray standing
37693-9|Femur - right X-ray standing
24708-0|Foot X-ray standing
26094-3|Foot - bilateral X-ray standing
26095-0|Foot - left X-ray standing
26096-8|Foot - right X-ray standing
37584-0|Great toe - left X-ray standing
38810-8|Great toe - right X-ray standing
24809-6|Knee X-ray standing
26085-1|Knee - bilateral X-ray standing
26086-9|Knee - left X-ray standing
26087-7|Knee - right X-ray standing
37204-5|Lower extremity X-ray standing
69264-0|Sacrum X-ray standing
37208-6|Spine Lumbar X-ray standing
69275-6|Spine Thoracic X-ray standing
38124-4|Spine Thoracic and Lumbar X-ray standing
37899-2|Tibia and Fibula X-ray standing
37209-4|Toes - left X-ray standing
37823-2|Toes - right X-ray standing
44233-5|Kidney - bilateral Scan W and WO Tc-99m DTPA IV
44232-7|Kidney - bilateral Scan W and WO Tc-99m Mertiatide IV
37579-0|Acromioclavicular Joint X-ray W and WO weight
37580-8|Acromioclavicular joint - bilateral X-ray W and WO weight
37581-6|Acromioclavicular joint - left X-ray W and WO weight
37663-2|Acromioclavicular joint - right X-ray W and WO weight
39651-5|Heart Scan W adenosine and W Tl-201 IV
38090-7|Breast - bilateral Mammogram W air
38091-5|Breast - left Mammogram W air
39059-1|Gastrointestine upper Fluoroscopy W air and barium contrast PO
24666-0|Colon Fluoroscopy W air and barium contrast PR
46357-0|Colon Fluoroscopy W air contrast PR
30633-2|Esophagus Fluoroscopy W barium contrast PO
42683-3|Gastrointestine upper Fluoroscopy W barium contrast PO
43574-3|Upper Gastrointestine and Small bowel Fluoroscopy W barium contrast PO
44227-7|Colon Fluoroscopy W barium contrast PR
37565-9|Unspecified body region Fluoroscopy W barium contrast via fistula
38092-3|Urinary bladder Fluoroscopy W chain and contrast intra bladder
41770-9|Gallbladder Scan W cholecystokinin and W radionuclide IV
43650-1|Liver and Biliary ducts and Gallbladder Scan W cholecystokinin and W radionuclide IV
30630-8|Head Cistern Fluoroscopy video W contrast
30824-7|Intercranial vessel and Neck Vessel Fluoroscopic angiogram W contrast
37585-7|Jejunum Fluoroscopy W contrast
38853-8|Lower extremity vessels - left Fluoroscopic angiogram W contrast
37765-5|Lower extremity vessels - right Fluoroscopic angiogram W contrast
37615-2|Pelvis vessels Fluoroscopic angiogram W contrast
37936-2|Peripheral vessels Fluoroscopic angiogram W contrast
37640-0|Renal vessels Fluoroscopic angiogram W contrast
64140-7|Renal vessels - left Fluoroscopic angiogram W contrast
64141-5|Renal vessels - right Fluoroscopic angiogram W contrast
38094-9|Spine.cavity Fluoroscopy W contrast
37973-5|Testicle vessels Fluoroscopy W contrast
37976-8|Upper extremity vessels Fluoroscopic angiogram W contrast
42014-1|Urinary Bladder and Urethra Fluoroscopy W contrast
37980-0|Vertebral vessels Fluoroscopic angiogram W contrast
37981-8|Visceral vessels Fluoroscopic angiogram W contrast
37575-8|Gallbladder X-ray W contrast and fatty meal PO
38101-2|Kidney X-ray W contrast antegrade
46376-0|Kidney - bilateral Fluoroscopy W contrast antegrade
38100-4|Urinary Bladder and Urethra Fluoroscopy W contrast antegrade
38102-0|Kidney X-ray W contrast antegrade via pyelostomy
25030-8|Abdominal Artieries Fluoroscopic angiogram W contrast IA
30832-0|Adrenal artery Fluoroscopic angiogram W contrast IA
30831-2|Adrenal artery - bilateral Fluoroscopic angiogram W contrast IA
37387-8|Adrenal artery - left Fluoroscopic angiogram W contrast IA
37939-6|Adrenal artery - right Fluoroscopic angiogram W contrast IA
38861-1|Ankle arteries - left Fluoroscopic angiogram W contrast IA
37941-2|Ankle arteries - right Fluoroscopic angiogram W contrast IA
24658-7|Aorta Fluoroscopic angiogram W contrast IA
30837-9|Aorta abdominal Fluoroscopic angiogram W contrast IA
24546-4|Aorta arch and Neck Fluoroscopic angiogram W contrast IA
37366-2|Abdominal Aorta and Arteries Fluoroscopic angiogram W contrast IA
69054-5|Aortic arch Fluoroscopic angiogram W contrast IA
37380-3|Aortic arch and Brachial artery Fluoroscopic angiogram W contrast IA
37381-1|Aortic arch and Carotid artery Fluoroscopic angiogram W contrast IA
37587-3|Aortic arch and Carotid artery - bilateral and Vertebral artery - bilateral Fluoroscopic angiogram W contrast IA
37588-1|Aortic arch and Carotid artery.common - bilateral Fluoroscopic angiogram W contrast IA
37589-9|Aortic arch and Carotid artery.common - left Fluoroscopic angiogram W contrast IA
37590-7|Aortic arch and Carotid artery.common - right Fluoroscopic angiogram W contrast IA
37591-5|Aortic arch and Carotid artery.external - bilateral Fluoroscopic angiogram W contrast IA
37592-3|Aortic arch and Carotid artery.external - left Fluoroscopic angiogram W contrast IA
37593-1|Aortic arch and Carotid artery.external - right Fluoroscopic angiogram W contrast IA
37594-9|Aortic arch and Carotid artery and Vertebral artery Fluoroscopic angiogram W contrast IA
37382-9|Aortic arch and Subclavian artery Fluoroscopic angiogram W contrast IA
37383-7|Aortic arch and Subclavian artery - left Fluoroscopic angiogram W contrast IA
38800-9|Aortic arch and Subclavian artery - right Fluoroscopic angiogram W contrast IA
37379-5|Aortic arch and Upper Extremity artery Fluoroscopic angiogram W contrast IA
37384-5|Aortic arch and Vertebral artery Fluoroscopic angiogram W contrast IA
37385-2|Aortic arch and Vertebral artery - left Fluoroscopic angiogram W contrast IA
37386-0|Aortic arch and Vertebral artery - right Fluoroscopic angiogram W contrast IA
24551-4|AV fistula Fluoroscopic angiogram W contrast IA
30828-8|Brachial artery Fluoroscopic angiogram W contrast IA
37388-6|Brachial artery - bilateral Fluoroscopic angiogram W contrast IA
24581-1|Brachial artery and Subclavian artery Fluoroscopic angiogram W contrast IA
69077-6|Brachiocephalic artery Fluoroscopic angiogram W contrast IA
37389-4|Bronchial artery Fluoroscopic angiogram W contrast IA
24617-3|Carotid artery Fluoroscopic angiogram W contrast IA
26079-4|Carotid artery - bilateral Fluoroscopic angiogram W contrast IA
39097-1|Carotid artery - bilateral and Cerebral artery - bilateral Fluoroscopic angiogram W contrast IA
39094-8|Carotid artery.cervical Fluoroscopic angiogram W contrast IA
39098-9|Carotid artery.cervical - bilateral Fluoroscopic angiogram W contrast IA
38863-7|Carotid artery.cervical - left Fluoroscopic angiogram W contrast IA
37945-3|Carotid artery.cervical - right Fluoroscopic angiogram W contrast IA
30821-3|Carotid artery.external Fluoroscopic angiogram W contrast IA
30820-5|Carotid artery.external - bilateral Fluoroscopic angiogram W contrast IA
37390-2|Carotid artery.external - left Fluoroscopic angiogram W contrast IA
37948-7|Carotid artery.external - right Fluoroscopic angiogram W contrast IA
38864-5|Carotid artery.internal - left Fluoroscopic angiogram W contrast IA
37952-9|Carotid artery.internal - right Fluoroscopic angiogram W contrast IA
26080-2|Carotid artery - left Fluoroscopic angiogram W contrast IA
26081-0|Carotid artery - right Fluoroscopic angiogram W contrast IA
39095-5|Carotid artery and Cerebral artery Fluoroscopic angiogram W contrast IA
38865-2|Carotid artery and Cerebral artery internal - left Fluoroscopic angiogram W contrast IA
37953-7|Carotid artery and Cerebral artery internal - right Fluoroscopic angiogram W contrast IA
38862-9|Carotid artery and Cerebral artery - left Fluoroscopic angiogram W contrast IA
37944-6|Carotid artery and Cerebral artery - right Fluoroscopic angiogram W contrast IA
37391-0|Carotid artery and Vertebral artery Fluoroscopic angiogram W contrast IA
37392-8|Carotid artery and Vertebral artery - bilateral Fluoroscopic angiogram W contrast IA
37393-6|Carotid artery+Vertebral artery - left Fluoroscopic angiogram W contrast IA
37943-8|Carotid artery+Vertebral artery - right Fluoroscopic angiogram W contrast IA
24622-3|Celiac artery Fluoroscopic angiogram W contrast IA
37403-3|Celiac artery and Gastric artery - left and Superior mesenteric artery Fluoroscopic angiogram W contrast IA
37394-4|Celiac artery and Superior mesenteric artery and Inferior mesenteric artery Fluoroscopic angiogram W contrast IA
37173-2|Cerebral artery Fluoroscopic angiogram W contrast IA
30891-6|Cervicocerebral artery Fluoroscopic angiogram W contrast IA
37174-0|Coronary arteries Fluoroscopic angiogram W contrast IA
37595-6|Coronary graft Fluoroscopic angiogram W contrast IA
30848-6|Extremity arteries Fluoroscopic angiogram W contrast IA
30849-4|Extremity arteries - bilateral Fluoroscopic angiogram W contrast IA
37395-1|Extremity arteries - left Fluoroscopic angiogram W contrast IA
37949-5|Extremity arteries - right Fluoroscopic angiogram W contrast IA
37175-7|Femoral artery Fluoroscopic angiogram W contrast IA
37176-5|Femoral artery and Popliteal artery Fluoroscopic angiogram W contrast IA
37397-7|Gastric artery Fluoroscopic angiogram W contrast IA
37398-5|Gastric artery - left Fluoroscopic angiogram W contrast IA
38801-7|Gastric artery - right Fluoroscopic angiogram W contrast IA
37399-3|Gastroduodenal artery Fluoroscopic angiogram W contrast IA
30822-1|Head artery - bilateral and Neck artery - bilateral Fluoroscopic angiogram W contrast IA
62448-6|Head artery.left+Neck artery.left Fluoroscopic angiogram W contrast IA
62449-4|Head artery.right+Neck artery.right Fluoroscopic angiogram W contrast IA
30823-9|Head artery and Neck artery Fluoroscopic angiogram W contrast IA
25076-1|Hepatic artery Fluoroscopic angiogram W contrast IA
43782-2|Iliac artery Fluoroscopic angiogram W contrast IA
37177-3|Iliac artery - bilateral Fluoroscopic angiogram W contrast IA
24862-5|Iliac artery Internal Fluoroscopic angiogram W contrast IA
37178-1|Iliac artery - left Fluoroscopic angiogram W contrast IA
37739-0|Iliac artery - right Fluoroscopic angiogram W contrast IA
37179-9|Inferior mesenteric artery Fluoroscopic angiogram W contrast IA
25079-5|Kidney arteries Fluoroscopic angiogram W contrast IA
37487-6|Lower extremity arteries Fluoroscopic angiogram W contrast IA
47986-5|Lower extremity arteries - left Fluoroscopic angiogram W contrast IA
47987-3|Lower extremity arteries - right Fluoroscopic angiogram W contrast IA
30829-6|Internal mammary artery Fluoroscopic angiogram W contrast IA
64995-4|Mammary artery.internal - left Fluoroscopic angiogram W contrast IA
65000-2|Mammary artery.internal - right Fluoroscopic angiogram W contrast IA
37401-7|Maxillary artery.internal Fluoroscopic angiogram W contrast IA
24833-6|Mesenteric artery Fluoroscopic angiogram W contrast IA
24860-9|Pancreatic artery Fluoroscopic angiogram W contrast IA
30833-8|Pelvis arteries Fluoroscopic angiogram W contrast IA
37935-4|Pelvis arteries and Lower extremity arteries - bilateral Fluoroscopic angiogram W contrast IA
24874-0|Peripheral arteries Fluoroscopic angiogram W contrast IA
44240-0|Peripheral arteries - bilateral Fluoroscopic angiogram W contrast IA
69249-1|Popliteal artery Fluoroscopic angiogram W contrast IA
37181-5|Popliteal artery - left Fluoroscopic angiogram W contrast IA
37778-8|Popliteal artery - right Fluoroscopic angiogram W contrast IA
37404-1|Pudendal artery.internal Fluoroscopic angiogram W contrast IA
39057-5|Pulmonary artery Fluoroscopic angiogram W contrast IA
30830-4|Pulmonary artery - bilateral Fluoroscopic angiogram W contrast IA
37182-3|Pulmonary artery - left Fluoroscopic angiogram W contrast IA
37779-6|Pulmonary artery - right Fluoroscopic angiogram W contrast IA
30834-6|Renal artery - bilateral Fluoroscopic angiogram W contrast IA
62446-0|Renal artery - left Fluoroscopic angiogram W contrast IA
62447-8|Renal artery - right Fluoroscopic angiogram W contrast IA
24925-0|Spinal artery Fluoroscopic angiogram W contrast IA
26082-8|Spinal artery - bilateral Fluoroscopic angiogram W contrast IA
26083-6|Spinal artery - left Fluoroscopic angiogram W contrast IA
26084-4|Spinal artery - right Fluoroscopic angiogram W contrast IA
24992-0|Splenic artery Fluoroscopic angiogram W contrast IA
24991-2|Splenic vein and Portal vein Fluoroscopic angiogram W contrast IA
37886-9|Subclavian artery Fluoroscopic angiogram W contrast IA
37405-8|Subclavian artery - bilateral Fluoroscopic angiogram W contrast IA
37406-6|Subclavian artery - left Fluoroscopic angiogram W contrast IA
37966-9|Subclavian artery - right Fluoroscopic angiogram W contrast IA
37180-7|Superior mesenteric artery Fluoroscopic angiogram W contrast IA
37402-5|Superior mesenteric artery and Inferior mesenteric artery Fluoroscopic angiogram W contrast IA
38119-4|Thoracic artery Fluoroscopic angiogram W contrast IA
37900-8|Tibial artery Fluoroscopic angiogram W contrast IA
37489-2|Tibioperoneal arteries Fluoroscopic angiogram W contrast IA
37977-6|Upper extremity arteries Fluoroscopic angiogram W contrast IA
37396-9|Upper extremity arteries - bilateral Fluoroscopic angiogram W contrast IA
37488-4|Upper extremity arteries - left Fluoroscopic angiogram W contrast IA
37967-7|Upper extremity arteries - right Fluoroscopic angiogram W contrast IA
24576-1|Urinary bladder arteries Fluoroscopic angiogram W contrast IA
37979-2|Uterine artery Fluoroscopic angiogram W contrast IA
37407-4|Vertebral artery - bilateral Fluoroscopic angiogram W contrast IA
37490-0|Vertebral artery - left Fluoroscopic angiogram W contrast IA
37968-5|Vertebral artery - right Fluoroscopic angiogram W contrast IA
42156-0|Vessels Fluoroscopic angiogram W contrast IA
25017-5|Urinary Bladder and Urethra Fluoroscopy W contrast intra bladder
43559-4|Urinary Bladder and Urethra Fluoroscopy W contrast intra bladder during voiding
37586-5|Penis Fluoroscopy W contrast intra corpus cavernosum
39054-2|Breast duct Mammogram W contrast intra duct
38095-6|Breast duct - bilateral Mammogram W contrast intra duct
38096-4|Breast duct - left Mammogram W contrast intra duct
38825-6|Breast duct - right Mammogram W contrast intra duct
30810-6|Lacrimal duct Fluoroscopy W contrast intra lacrimal duct
38098-0|Lacrimal duct - bilateral Fluoroscopy W contrast intra lacrimal duct
38099-8|Lacrimal duct - left Fluoroscopy W contrast intra lacrimal duct
38827-2|Lacrimal duct - right Fluoroscopy W contrast intra lacrimal duct
24845-0|Neck Fluoroscopy W contrast intra larynx
30850-2|Extremity lymphatics Fluoroscopy W contrast intra lymphatic
30851-0|Extremity lymphatics - bilateral Fluoroscopy W contrast intra lymphatic
37599-8|Extremity lymphatics - left Fluoroscopy W contrast intra lymphatic
38812-4|Extremity lymphatics - right Fluoroscopy W contrast intra lymphatic
24827-8|Lymphatics Fluoroscopy W contrast intra lymphatic
30839-5|Lymphatics abdominal Fluoroscopy W contrast intra lymphatic
30840-3|Lymphatics abdominal - bilateral Fluoroscopy W contrast intra lymphatic
37597-2|Lymphatics abdominal and Lymphatics pelvic Fluoroscopy W contrast intra lymphatic
37598-0|Lymphatics abdominal and Lymphatics pelvic - bilateral Fluoroscopy W contrast intra lymphatic
37596-4|Lymphatics abdominal and Lymphatics pelvic - left Fluoroscopy W contrast intra lymphatic
38811-6|Lymphatics abdominal and Lymphatics pelvic - right Fluoroscopy W contrast intra lymphatic
37600-4|Lymphatics - left Fluoroscopy W contrast intra lymphatic
39510-3|Lymphatics pelvic Fluoroscopy W contrast intra lymphatic
37601-2|Lymphatics pelvic - bilateral Fluoroscopy W contrast intra lymphatic
38813-2|Lymphatics - right Fluoroscopy W contrast intra lymphatic
39148-2|Breast duct Mammogram W contrast intra multiple ducts
39146-6|Breast duct - bilateral Mammogram W contrast intra multiple ducts
39145-8|Breast duct - left Mammogram W contrast intra multiple ducts
39147-4|Breast duct - right Mammogram W contrast intra multiple ducts
24661-1|Pleural space Fluoroscopy W contrast intra pleural space
38116-0|Parotid gland Fluoroscopy W contrast intra salivary duct
38097-2|Parotid gland - left Fluoroscopy W contrast intra salivary duct
38826-4|Parotid gland - right Fluoroscopy W contrast intra salivary duct
24902-9|Salivary gland Fluoroscopy W contrast intra salivary duct
26067-9|Salivary gland - bilateral Fluoroscopy W contrast intra salivary duct
26068-7|Salivary gland - left Fluoroscopy W contrast intra salivary duct
26069-5|Salivary gland - right Fluoroscopy W contrast intra salivary duct
38153-3|Submandibular gland Fluoroscopy W contrast intra salivary duct
48698-5|Submandibular gland - bilateral Fluoroscopy W contrast intra salivary duct
42460-6|Submandibular gland - left Fluoroscopy W contrast intra salivary duct
48696-9|Submandibular gland - right Fluoroscopy W contrast intra salivary duct
24912-8|Sinus tract Fluoroscopy W contrast intra sinus tract
24552-2|Stent Fluoroscopy W contrast intra stent
25016-7|Urethra Fluoroscopy W contrast intra urethra
39151-6|Vas deferens Fluoroscopy W contrast intra vas deferens
37183-1|Ankle Fluoroscopy W contrast intraarticular
37184-9|Ankle - bilateral Fluoroscopy W contrast intraarticular
37185-6|Ankle - left Fluoroscopy W contrast intraarticular
37942-0|Ankle - right Fluoroscopy W contrast intraarticular
37186-4|Elbow Fluoroscopy W contrast intraarticular
37187-2|Elbow - bilateral Fluoroscopy W contrast intraarticular
37188-0|Elbow - left Fluoroscopy W contrast intraarticular
37947-9|Elbow - right Fluoroscopy W contrast intraarticular
24764-3|Hip Fluoroscopy W contrast intraarticular
26070-3|Hip - bilateral Fluoroscopy W contrast intraarticular
26071-1|Hip - left Fluoroscopy W contrast intraarticular
26072-9|Hip - right Fluoroscopy W contrast intraarticular
24800-5|Knee Fluoroscopy W contrast intraarticular
26073-7|Knee - bilateral Fluoroscopy W contrast intraarticular
26074-5|Knee - left Fluoroscopy W contrast intraarticular
26075-2|Knee - right Fluoroscopy W contrast intraarticular
37647-5|Sacroiliac Joint Fluoroscopy W contrast intraarticular
37189-8|Sacroiliac joint - bilateral Fluoroscopy W contrast intraarticular
37190-6|Sacroiliac joint - left Fluoroscopy W contrast intraarticular
37785-3|Sacroiliac joint - right Fluoroscopy W contrast intraarticular
24910-2|Shoulder Fluoroscopy W contrast intraarticular
26076-0|Shoulder - bilateral Fluoroscopy W contrast intraarticular
26077-8|Shoulder - left Fluoroscopy W contrast intraarticular
26078-6|Shoulder - right Fluoroscopy W contrast intraarticular
37901-6|Temporomandibular joint Fluoroscopy W contrast intraarticular
37409-0|Temporomandibular joint - bilateral Fluoroscopy W contrast intraarticular
37410-8|Temporomandibular joint - left Fluoroscopy W contrast intraarticular
37818-2|Temporomandibular joint - right Fluoroscopy W contrast intraarticular
25034-0|Wrist Fluoroscopy W contrast intraarticular
37570-9|Wrist - bilateral Fluoroscopy W contrast intraarticular
37571-7|Wrist - left Fluoroscopy W contrast intraarticular
37641-8|Wrist - right Fluoroscopy W contrast intraarticular
37191-4|Joint Fluoroscopy W contrast intraarticular
24825-2|Lung X-ray W contrast intrabronchial
30813-0|Lung - bilateral X-ray W contrast intrabronchial
64996-2|Lung - left X-ray W contrast intrabronchial
64997-0|Lung - right X-ray W contrast intrabronchial
37192-2|Spine Cervical Fluoroscopy W contrast intradisc
37193-0|Spine Lumbar Fluoroscopy W contrast intradisc
70933-7|Spine Thoracic Fluoroscopy W contrast intradisc
25022-5|Uterus and Fallopian tubes Fluoroscopy W contrast intrauterine
30811-4|Posterior fossa Fluoroscopy W contrast IT
24947-4|Spine Cervical Fluoroscopy W contrast IT
38103-8|Spine Cervical and Spine Lumbar Fluoroscopy W contrast IT
30808-0|Spine Cervical and Thoracic and Lumbar Fluoroscopy W contrast IT
38104-6|Spine.epidural space Fluoroscopy W contrast IT
24974-8|Spine Lumbar Fluoroscopy W contrast IT
24985-4|Spine Thoracic Fluoroscopy W contrast IT
69066-9|Abdominal vessels Fluoroscopic angiogram W contrast IV
30843-7|Adrenal vein Fluoroscopic angiogram W contrast IV
37602-0|Adrenal vein left Fluoroscopic angiogram W contrast IV
30844-5|Adrenal vein - bilateral Fluoroscopic angiogram W contrast IV
37940-4|Adrenal vein - right Fluoroscopic angiogram W contrast IV
58746-9|AV fistula Fluoroscopic angiogram W contrast IV
24569-6|AV shunt Fluoroscopic angiogram W contrast IV
37411-6|Azygos vein Fluoroscopic angiogram W contrast IV
24573-8|Biliary ducts and Gallbladder X-ray W contrast IV
37195-5|Cerebral vein Fluoroscopic angiogram W contrast IV
30819-7|Epidural veins Fluoroscopic angiogram W contrast IV
39055-9|Extremity veins Fluoroscopic angiogram W contrast IV
37412-4|Extremity veins - bilateral Fluoroscopic angiogram W contrast IV
37413-2|Extremity veins - left Fluoroscopic angiogram W contrast IV
37950-3|Extremity veins - right Fluoroscopic angiogram W contrast IV
42157-8|Extremity vessels Fluoroscopic angiogram W contrast IV
37416-5|Femoral vein Fluoroscopic angiogram W contrast IV
39093-0|Hepatic veins Fluoroscopic angiogram W contrast IV
37421-5|Inferior mesenteric vein Fluoroscopic angiogram W contrast IV
37419-9|Intraosseous veins Fluoroscopic angiogram W contrast IV
37197-1|Jugular vein Fluoroscopic angiogram W contrast IV
37420-7|Jugular vein - left Fluoroscopic angiogram W contrast IV
37954-5|Jugular vein - right Fluoroscopic angiogram W contrast IV
37607-9|Kidney X-ray W contrast IV
24788-2|Kidney - bilateral X-ray W contrast IV
37414-0|Lower extremity veins - bilateral Fluoroscopic angiogram W contrast IV
37196-3|Lower extremity veins - left Fluoroscopic angiogram W contrast IV
37767-1|Lower extremity veins - right Fluoroscopic angiogram W contrast IV
37574-1|Lower extremity vessels Fluoroscopic angiogram W contrast IV
30825-4|Orbit veins Fluoroscopic angiogram W contrast IV
37422-3|Orbit veins - left Fluoroscopic angiogram W contrast IV
37958-6|Orbit veins - right Fluoroscopic angiogram W contrast IV
30852-8|Peripheral veins - bilateral Fluoroscopic angiogram W contrast IV
24685-0|Peripheral veins Fluoroscopic angiogram W contrast IV
69250-9|Portal vein Fluoroscopic angiogram W contrast IV
30847-8|Renal vein Fluoroscopic angiogram W contrast IV
30846-0|Renal vein - bilateral Fluoroscopic angiogram W contrast IV
37423-1|Renal vein - left Fluoroscopic angiogram W contrast IV
37959-4|Renal vein - right Fluoroscopic angiogram W contrast IV
30827-0|Sagittal sinus vein Fluoroscopic angiogram W contrast IV
65803-9|Sagittal sinus vein - left Fluoroscopic angiogram W contrast IV
65802-1|Sagittal sinus and Jugular veins - left Fluoroscopic angiogram W contrast IV
65804-7|Sagittal sinus vein - right Fluoroscopic angiogram W contrast IV
65805-4|Sagittal sinus and Jugular veins - right Fluoroscopic angiogram W contrast IV
30826-2|Sagittal sinus and Jugular veins Fluoroscopic angiogram W contrast IV
37969-3|Sinus vein Fluoroscopic angiogram W contrast IV
37970-1|Splenic vein Fluoroscopic angiogram W contrast IV
37971-9|Subclavian vein Fluoroscopic angiogram W contrast IV
37972-7|Superior mesenteric vein Fluoroscopic angiogram W contrast IV
24550-6|Upper extremity veins Fluoroscopic angiogram W contrast IV
37415-7|Upper extremity veins - bilateral Fluoroscopic angiogram W contrast IV
38859-5|Upper extremity veins - left Fluoroscopic angiogram W contrast IV
37824-0|Upper extremity veins - right Fluoroscopic angiogram W contrast IV
25023-3|Vein Fluoroscopic angiogram W contrast IV
26064-6|Vein - bilateral Fluoroscopic angiogram W contrast IV
26065-3|Vein - left Fluoroscopic angiogram W contrast IV
26066-1|Vein - right Fluoroscopic angiogram W contrast IV
25025-8|Vena cava Fluoroscopic angiogram W contrast IV
30845-2|Inferior vena cava Fluoroscopic angiogram W contrast IV
30645-6|Superior vena cava Fluoroscopic angiogram W contrast IV
43554-5|vessels - left Fluoroscopic angiogram W contrast IV
39096-3|Hepatic veins Fluoroscopic angiogram W contrast IV and W hemodynamics
43783-0|Renal vein Fluoroscopic angiogram W contrast IV and W renin sampling
25080-3|Renal vein - bilateral Fluoroscopic angiogram W contrast IV and W renin sampling
30816-3|Peritoneum Fluoroscopic angiogram W contrast percutaneous
24575-3|Biliary ducts and Gallbladder Fluoroscopy W contrast percutaneous transhepatic
37200-3|Chest X-ray W contrast PO
37199-7|Chest Fluoroscopy W contrast PO
37198-9|Esophagus X-ray W contrast PO
24678-5|Esophagus Fluoroscopy W contrast PO
24712-2|Gallbladder X-ray W contrast PO
42459-8|Gastrointestine upper Fluoroscopy W contrast PO
24924-3|Small bowel Fluoroscopy W contrast PO
24673-6|Duodenum Fluoroscopy W contrast PO and hypotonic agent per ng
24681-9|Esophagus and Hypopharynx Fluoroscopy video W contrast PO during swallowing
24667-8|Colon Fluoroscopy W contrast PR
24894-8|Rectum and Urinary bladder Fluoroscopy W contrast PR and intra bladder during defecation and voiding
39363-7|Fistula Fluoroscopy W contrast retrograde
38105-3|Kidney X-ray W contrast retrograde
39349-6|Kidney - bilateral Fluoroscopy W contrast retrograde
30761-1|Kidney - bilateral Fluoroscopy W contrast retrograde via urethra
38873-6|Kidney - left and Collecting system Fluoroscopy W contrast retrograde via urethra
38113-7|Kidney - right and Collecting system Fluoroscopy W contrast retrograde via urethra
25020-9|Urinary Bladder and Urethra Fluoroscopy W contrast retrograde via urethra
30841-1|Portal vein Fluoroscopic angiogram W contrast transhepatic
30842-9|Portal vein Fluoroscopic angiogram W contrast transhepatic and W hemodynamics
37566-7|Unspecified body region Fluoroscopy W contrast via catheter
37567-5|Colon Fluoroscopy W contrast via colostomy
37568-3|Unspecified body region Fluoroscopy W contrast via fistula
69272-3|Small bowel Fluoroscopy W contrast via ileostomy
24780-9|Kidney - bilateral Fluoroscopy W contrast via nephrostomy tube
38872-8|Kidney - left and Collecting system Fluoroscopy W contrast via nephrostomy tube
38112-9|Kidney - right and Collecting system Fluoroscopy W contrast via nephrostomy tube
37569-1|Urinary bladder Fluoroscopy W contrast via suprapubic tube
30647-2|Biliary ducts and Gallbladder Fluoroscopy W contrast via T-tube
39696-0|Lung Scan W depreotide and W radionuclide IV
42161-0|Heart Scan W dobutamine and W radionuclide IV
39652-3|Heart Scan W dobutamine and W Tl-201 IV
42383-0|Gallbladder X-ray W double dose contrast PO
42690-8|Spine X-ray W flexion and W extension
24945-8|Spine Cervical X-ray W flexion and W extension
24971-4|Spine Lumbar X-ray W flexion and W extension
43481-1|Joint X-ray W flexion and W extension
30785-0|Foot X-ray W forced dorsiflexion
43461-3|Kidney - bilateral Scan W furosemide and W radionuclide IV
39688-7|Scan W GA-67 IV
24679-3|Esophagus Fluoroscopy W gastrografin PO
42684-1|Gastrointestine upper Fluoroscopy W gastrografin PO
42681-7|Colon Fluoroscopy W gastrografin PR
37576-6|Unspecified body region Fluoroscopy W gastrografin via fistula
39850-3|Kidney - bilateral Scan W I-131 IV
25007-6|Thyroid Scan W I-131 IV
39841-2|Scan W I-131 MIBG IV
39857-8|Adrenal gland Scan W I-131 MIBG IV
39624-2|Adrenal gland Scan W I-131 NP59 IV
24770-0|Joint Scan W In-111 intrajoint
39846-1|Scan W In-111 Satumomab IV
39738-0|Abdomen Scan W In-111 Satumomab IV
25032-4|Bone Scan W In-111 tagged WBC IV
42708-8|Scan W In-111 tiuxetan IV
30736-3|Chest X-ray W inspiration and expiration
24682-7|Esophagus and Hypopharynx Fluoroscopy video W liquid and paste contrast PO during swallowing
37556-8|Ankle X-ray W manual stress
37557-6|Ankle - bilateral X-ray W manual stress
37558-4|Ankle - left X-ray W manual stress
37673-1|Ankle - right X-ray W manual stress
37559-2|Foot - left X-ray W manual stress
37705-1|Foot - right X-ray W manual stress
37560-0|Knee X-ray W manual stress
37561-8|Knee - bilateral X-ray W manual stress
37562-6|Knee - left X-ray W manual stress
37753-1|Knee - right X-ray W manual stress
37563-4|Thumb - bilateral X-ray W manual stress
37564-2|Thumb - left X-ray W manual stress
37814-1|Thumb - right X-ray W manual stress
39056-7|Unspecified body region X-ray W manual stress
38093-1|Chest X-ray W nipple markers
39670-5|Lacrimal duct Scan W radionuclide intra lacrimal duct
64051-6|Breast lymphatics - left Scan W radionuclide intra lymphatic
64052-4|Breast lymphatics - right Scan W radionuclide intra lymphatic
24826-0|Lymphatics Scan W radionuclide intra lymphatic
24663-7|Head Cistern Scan W radionuclide IT
42158-6|Adrenal gland Scan
42776-5|AV shunt Scan
25031-6|Bone Scan
24730-4|Brain Scan
39643-2|Brain veins Scan
39646-5|Breast Scan
39650-7|Heart Scan
24776-7|Kidney - bilateral Scan
30877-5|Kidney - bilateral and Renal vessels Scan
24804-7|Knee Scan
26088-5|Knee - bilateral Scan
26089-3|Knee - left Scan
26090-1|Knee - right Scan
39693-7|Liver Scan
39694-5|Liver transplant Scan
43557-8|Liver and Biliary ducts and Gallbladder Scan
39897-4|Liver and Lung Scan
39877-6|Liver and Spleen Scan
39629-1|Meckels diverticulum Scan
39737-2|Neck Scan
39739-8|Pancreas Scan
39742-2|Parathyroid Scan
39619-2|Pulmonary system Scan
43669-1|Renal vessels Scan
39747-1|Salivary gland Scan
30696-9|Scrotum and Testicle Scan
39751-3|Spleen Scan
30695-1|Thyroid Scan
25018-3|Urinary bladder Scan
39626-7|Vein - bilateral Scan
49118-3|Unspecified body region Scan
39939-4|Joint Scan
39671-3|Rectum Scan W radionuclide PO
39752-1|Spleen Scan W radionuclide tagged heat damaged RBC IV
24773-4|Kidney - bilateral Scan W radionuclide transplant scan
30713-2|Spine X-ray W right bending and W left bending
42413-5|Spine Lumbar X-ray W right bending and W left bending
43651-9|Liver and Biliary ducts and Gallbladder Scan W sincalide and W radionuclide IV
39820-6|Bone Scan W SM153 IV
39666-3|Heart Scan W stress and W 201 Th IV
39667-1|Heart Scan W stress and W radionuclide IV
69231-9|Heart Scan W stress and W Tc-99m IV
69232-7|Heart Scan W stress and W Tc-99m Sestamibi IV
24819-5|Liver and Spleen Scan W Tc-99m calcium colloid IV
39744-8|Prostate Scan W Tc-99m capromab pendatide IV
39674-7|Gallbladder Scan W Tc-99m DISIDA IV
41771-7|Kidney - bilateral Scan W Tc-99m DMSA IV
39625-9|Artery Scan W Tc-99m DTPA IA
39745-5|Kidney - bilateral Scan W Tc-99m DTPA IV
43667-5|Kidney - bilateral and Renal vessels Scan W Tc-99m DTPA IV
39753-9|Scrotum and Testicle Scan W Tc-99m DTPA IV
39765-3|Vein Scan W Tc-99m DTPA IV
39642-4|Brain Scan W Tc-99m glucoheptonate IV
44234-3|Kidney - bilateral Scan W Tc-99m glucoheptonate IV
39766-1|Vein Scan W Tc-99m HDP IV
39812-3|Bone Scan W Tc-99m HMPAO IV
39630-9|Brain Scan W Tc-99m HMPAO IV
39757-0|Thyroid Scan W Tc-99m IV
24831-0|Meckels diverticulum Scan W Tc-99m M04 IV
44141-0|Liver and Spleen Scan W Tc-99m MAA IV
44142-8|Bone Scan W Tc-99m medronate IV
39746-3|Kidney - bilateral Scan W Tc-99m Mertiatide IV
69233-5|Parotid gland Scan W Tc-99m pertechnetate IV
25001-9|Scrotum and Testicle Scan W Tc-99m pertechnetate IV
26091-9|Scrotum and Testicle - bilateral Scan W Tc-99m pertechnetate IV
26092-7|Scrotum and Testicle - left Scan W Tc-99m pertechnetate IV
26093-5|Scrotum and Testicle - right Scan W Tc-99m pertechnetate IV
44146-9|Bone marrow Scan W Tc-99m SC IV
39689-5|Gastrointestine Scan W Tc-99m SC IV
69230-1|Liver Scan W Tc-99m SC IV
39764-6|Vein Scan W Tc-99m SC IV
24683-5|Esophagus and Stomach Scan W Tc-99m SC PO
44145-1|Parathyroid Scan W Tc-99m Sestamibi IV
39756-2|Thyroid Scan W Tc-99m Sestamibi IV
24714-8|Gastrointestine Scan W Tc-99m tagged RBC IV
44143-6|Heart Scan W Tc-99m tagged RBC IV
39690-3|Liver Scan W Tc-99m tagged RBC IV
42700-5|Bone Scan W Tc-99m tagged WBC IV
24751-0|Parathyroid Scan W TI-201 subtraction Tc-99m IV
39635-8|Brain Scan W Tl-201 IV
51389-5|Breast Scan W Tl-201 IV
42012-5|Gastrointestine upper Fluoroscopy W water soluble contrast PO
24669-4|Colon Fluoroscopy W water soluble contrast PR
37577-4|Acromioclavicular Joint X-ray W weight
37578-2|Acromioclavicular joint - bilateral X-ray W weight
44144-4|Liver Scan W Xe-133 inhaled
37582-4|Acromioclavicular Joint X-ray WO weight
69055-2|Acromioclavicular joint - bilateral X-ray WO weight
"""