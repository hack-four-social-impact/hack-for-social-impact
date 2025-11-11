import { useState } from "react";
import {
  Box,
  Button,
  Chip,
  Divider,
  Drawer,
  InputAdornment,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Paper,
  TextField,
  Typography,
  Avatar,
  Modal,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import FileDownloadOutlinedIcon from '@mui/icons-material/FileDownloadOutlined';
import UploadFileOutlinedIcon from '@mui/icons-material/UploadFileOutlined';
import PdfUploadModal from "../PdfUploadModal";
import mockData from "../mockData.json";
import { PDFExporter, type MockParoleData } from "../utils/pdfExporter";
import type { ClientData, SidebarClient } from "../types/client";
import type { ParoleSummaryResponse } from "../services/api";
import innocenClaimData from '../innocenceClaimData.json';


function Dashboard() {
  // Initialize with mock data
  const [allClientData, setAllClientData] = useState<ClientData[]>(mockData as ClientData[]);

  // Convert client data to sidebar clients
  const clients: SidebarClient[] = allClientData.map(item => ({
    id: item.id,
    name: item.demographics.clientInfo.name,
    cdcrNumber: item.demographics.clientInfo.cdcrNumber,
    dateOfBirth: item.demographics.clientInfo.dateOfBirth,
    contactInfo: item.demographics.clientInfo.contactInfo,
    status: "active", // You can adjust status logic if needed
  }));

  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState<SidebarClient>(clients[0]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [uploadSuccess, setUploadSuccess] = useState<string | null>(null);
  const [isInnocenceModalOpen, setIsInnocenceModalOpen] = useState(false);

  const filteredClients = clients.filter(
    c =>
      c.name.toLowerCase().includes(search.toLowerCase()) || c.cdcrNumber.toLowerCase().includes(search.toLowerCase())
  );

  // Find selected client's full data
  const selectedData = allClientData.find(item => item.demographics.clientInfo.name === selected.name);

  // Handle new PDF upload
  const handleNewUpload = (uploadResult: ParoleSummaryResponse) => {
    console.log("Processing new upload:", uploadResult);

    // Generate a new ID (simple increment)
    const newId = allClientData.length > 0 ? Math.max(...allClientData.map(item => item.id)) + 1 : 1;

    const newClientData: ClientData = {
      id: newId,
      success: uploadResult.success,
      filename: uploadResult.filename,
      file_size: uploadResult.file_size,
      extracted_text_length: uploadResult.extracted_text_length,
      markdown_summary: uploadResult.markdown_summary,
      demographics: uploadResult.demographics,
      summary_type: uploadResult.summary_type,
    };

    // Add to client data (put new clients at the top)
    setAllClientData(prev => [newClientData, ...prev]);

    // Auto-select the newly uploaded client
    const newSidebarClient: SidebarClient = {
      id: newId,
      name: uploadResult.demographics.clientInfo.name || `Client from ${uploadResult.filename}`,
      cdcrNumber: uploadResult.demographics.clientInfo.cdcrNumber || "N/A",
      dateOfBirth: uploadResult.demographics.clientInfo.dateOfBirth || "N/A",
      contactInfo: uploadResult.demographics.clientInfo.contactInfo || "N/A",
      status: "active",
    };

    setSelected(newSidebarClient);

    // Show success message
    setUploadSuccess(`Successfully processed ${uploadResult.filename}!`);
    // Clear success message after 5 seconds
    setTimeout(() => setUploadSuccess(null), 5000);

    console.log("Successfully added new client:", newSidebarClient);
  };

  // Handle PDF export
  const handleExportPDF = () => {
    if (selectedData) {
      const exporter = new PDFExporter();
      exporter.exportMockDataToPDF(selectedData as MockParoleData);
    }
  };

  // Use innocence claim data from JSON
  const innocenceFindings = innocenClaimData.innocence_analysis.findings;

  // Helper to format speaker name
  const formatSpeakerName = (name: string) =>
    name
      .split(' ')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');

  // Helper to format category
  const formatCategory = (cat: string) =>
    cat
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');

  // Helper to format client name to normal capitalization
  const formatClientName = (name: string) =>
    name
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');

  return (
    <Box sx={{ display: "flex", height: "100vh", bgcolor: "#fff" }}>
      {/* Sidebar */}
      <Drawer
        variant="permanent"
        sx={{
          width: 300,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: {
            width: 350,
            boxSizing: "border-box",
            bgcolor: "#f7f8fa",
            borderRight: "1px solid #e4e7ec",
          },
        }}
      >
        <Box sx={{ p: 3, pb: 1 }}>
          <Typography variant="h5" fontWeight={700} sx={{ mb: 2, textAlign: "left" }}>
            Clients
          </Typography>
          <TextField
            fullWidth
            placeholder="Search clients..."
            variant="outlined"
            size="small"
            value={search}
            onChange={e => setSearch(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon color="action" />
                </InputAdornment>
              ),
            }}
            sx={{ bgcolor: "#fff" }}
          />
        </Box>
        <List sx={{ px: 2, flex: 1 }}>
          {filteredClients.map(client => (
            <ListItem
              key={client.id}
              onClick={() => setSelected(client)}
              sx={{
                mb: 1,
                borderRadius: 2,
                bgcolor: selected.id === client.id ? "#ebeff6ff" : "transparent",
                boxShadow: selected.id === client.id ? 1 : 0,
                cursor: "pointer",
                transition: "background 0.2s",
              }}
            >
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: (theme) => theme.palette.primary.main, color: '#fff' }}>
                  {formatClientName(client.name).split(" ").map(n => n[0]).join("")}
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", width: "100%" }}>
                    <Typography fontWeight={600}>{formatClientName(client.name)}</Typography>
                    <Chip
                      label={client.status}
                      color={client.status === "active" ? "primary" : "default"}
                      size="small"
                      sx={{ textTransform: "capitalize", fontWeight: 500 }}
                    />
                  </Box>
                }
                secondary={
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      CDCR #{client.cdcrNumber}
                    </Typography>
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
        <Box sx={{ px: 2, pb: 3 }}>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            sx={{ borderRadius: 2, py: 1.5, fontWeight: 600, fontSize: 16 }}
            onClick={() => setIsModalOpen(true)}
          >
            <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <UploadFileOutlinedIcon sx={{ fontSize: 20, mr: 1 }} /> Upload Documents
            </span>
          </Button>
        </Box>
      </Drawer>

      {/* Main Content */}
      <Box sx={{ flex: 1, p: 4 }}>
        {/* Success Message */}
        {uploadSuccess && (
          <Paper
            elevation={1}
            sx={{
              p: 2,
              mb: 3,
              backgroundColor: "#f0f9ff",
              border: "1px solid #0ea5e9",
              borderRadius: 2,
              maxWidth: 800,
              mx: "auto",
            }}
          >
            <Typography variant="body1" sx={{ color: "#0369a1", fontWeight: 500, textAlign: "center" }}>
              ✅ {uploadSuccess}
            </Typography>
          </Paper>
        )}

        {/* Document Analysis Section */}
        <Paper elevation={2} sx={{ p: 4, borderRadius: 3, maxWidth: 800, mx: 'auto', boxShadow: '0 2px 12px rgba(0,0,0,0.04)' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
            <Box>
              <Typography variant="h5" fontWeight={900} sx={{ color: '#1a1a1a', textAlign: 'left', mb: 0 }}>
                Case Analysis
              </Typography>
              <Typography variant="subtitle1" color="#6b7280" sx={{ fontWeight: 500, textAlign: 'left', mt: 0.5 }}>
                Comprehensive legal document summary
              </Typography>
            </Box>
            <Box sx={{ display: 'flex', gap: 2 }}>
              <Button
                variant="outlined"
                color="secondary"
                sx={{
                  borderRadius: 2,
                  textTransform: 'none',
                  fontWeight: 600,
                  px: 2,
                  py: 1,
                  bgcolor: '#fff',
                  borderColor: (theme) => theme.palette.primary.main,
                  color: (theme) => theme.palette.primary.main,
                  '&:hover': {
                    bgcolor: '#f0f6ff',
                    borderColor: (theme) => theme.palette.primary.main,
                    color: (theme) => theme.palette.primary.main,
                  },
                }}
                onClick={() => setIsInnocenceModalOpen(true)}
              >
                Innocence Claim
              </Button>
              {/* <Button variant="contained" color="primary" sx={{ borderRadius: 2, textTransform: 'none', fontWeight: 600, px: 2, py: 1 }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <FileDownloadOutlinedIcon sx={{ fontSize: 20, mr: 1 }} /> Export
                </span>
              </Button> */}
              <Button
                variant="contained"
                color="primary"
                sx={{ borderRadius: 2, textTransform: "none", fontWeight: 600, px: 2, py: 1 }}
                onClick={handleExportPDF}
              >
                <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <FileDownloadOutlinedIcon sx={{ fontSize: 20, mr: 1 }} /> Export
                </span>
                {/* <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                  <FileDownloadOutlinedIcon sx={{ fontSize: 20, mr: 1 }} /> Export
                </span> */}
              </Button>
            </Box>
          </Box>
          <Typography variant="h6" fontWeight={700} sx={{ color: '#1a1a1a', textAlign: 'left', mb: 1.5 }}>
            Client Information
          </Typography>
          <Box sx={{ display: "flex", gap: 6, mt: 2, mb: 3 }}>
            <Box>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Client's Name & CDCR No.
              </Typography>
              <Typography fontWeight={600} sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.clientInfo.name} ({selectedData?.demographics.clientInfo.cdcrNumber})
              </Typography>
            </Box>
            <Box>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Contact Information
              </Typography>
              <Typography fontWeight={600} sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.clientInfo.contactInfo}
              </Typography>
            </Box>
            <Box>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Date of Birth
              </Typography>
              <Typography fontWeight={600} sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.clientInfo.dateOfBirth}
              </Typography>
            </Box>
          </Box>
          <Divider sx={{ mb: 3 }} />
          {/* Introduction */}
          <Typography variant="h6" fontWeight={700} sx={{ mb: 1.5, color: "#1a1a1a", textAlign: "left" }}>
            Introduction
          </Typography>
          <Typography sx={{ mb: 3, color: "#1a1a1a", fontWeight: 400, textAlign: "left" }}>
            {selectedData?.demographics.introduction.shortSummary}
          </Typography>
          <Divider sx={{ mb: 3 }} />
          {/* Evidence Used to Convict */}
          <Typography variant="h6" fontWeight={700} sx={{ mb: 1.5, color: "#1a1a1a", textAlign: "left" }}>
            Evidence Used to Convict
          </Typography>
          <ul style={{ marginBottom: 24, marginTop: 0, paddingLeft: 24, textAlign: "left" }}>
            {selectedData?.demographics.evidenceUsedToConvict.map((evidence, idx) => (
              <li key={idx} style={{ marginBottom: 8, color: "#1a1a1a", fontWeight: 400 }}>
                {evidence}
              </li>
            ))}
          </ul>
          <Divider sx={{ mb: 3 }} />

          {/* Conviction Information */}
          <Typography variant="h6" fontWeight={700} sx={{ mb: 1.5, color: "#1a1a1a", textAlign: "left" }}>
            Conviction Information
          </Typography>
          <Box sx={{ display: 'flex', gap: 6, mb: 3 }}>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Date of Crime
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.convictionInfo.dateOfCrime}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Location of Crime
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.convictionInfo.locationOfCrime}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Date of Arrest
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.convictionInfo.dateOfArrest}
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', gap: 6, mb: 3 }}>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Charges
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.convictionInfo.charges}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Date of Conviction
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.convictionInfo.dateOfConviction}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Sentence Length
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.convictionInfo.sentenceLength}
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', gap: 6, mb: 3 }}>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                County
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.convictionInfo.county}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Trial or Plea
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.convictionInfo.trialOrPlea}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }} />
          </Box>
          <Divider sx={{ mb: 3 }} />
          {/* Appeal Info */}
          <Typography variant="h6" fontWeight={700} sx={{ mb: 1.5, color: "#1a1a1a", textAlign: "left" }}>
            Appeal Information
          </Typography>
          <Box sx={{ display: "flex", flexWrap: "wrap", gap: 6, mb: 3 }}>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Direct Appeal Filed
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.appealInfo.directAppealFiled}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Appellate Court Case Number
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.appealInfo.appellateCourtCaseNumber}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Date Decided
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.appealInfo.dateDecided}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Box sx={{ border: '2px solid #b3d4fc', borderRadius: 4, px: 3, py: 1.5, mx: 1, mb: 2, bgcolor: '#f7faff' }}>
                <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: 'center' }}>Result</Typography>
                <Typography sx={{ color: '#1a1a1a', textAlign: 'center' }}>{selectedData?.demographics.appealInfo.result}</Typography>
              </Box>
            </Box>
            {Array.isArray(selectedData?.demographics.appealInfo?.habenasFilings) &&
              selectedData.demographics.appealInfo.habenasFilings.length > 0 && (
                <Box sx={{ flex: 1, minWidth: 200 }}>
                  <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                    Habeas Filings
                  </Typography>
                  <Box>
                    {selectedData.demographics.appealInfo.habenasFilings.map((filing, idx) => (
                      <Typography key={idx} sx={{ color: "#1a1a1a", textAlign: "left" }}>
                        {filing}
                      </Typography>
                    ))}
                  </Box>
                </Box>
              )}
          </Box>
          <Divider sx={{ mb: 3 }} />
          {/* Attorney Info */}
          <Typography variant="h6" fontWeight={700} sx={{ mb: 1.5, color: "#1a1a1a", textAlign: "left" }}>
            Attorney Information
          </Typography>
          <Box sx={{ display: 'flex', gap: 6, mb: 3 }}>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Current Attorney
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.attorneyInfo.currentAttorneyForIncarceratedPerson?.name} (
                {selectedData?.demographics.attorneyInfo.currentAttorneyForIncarceratedPerson?.title})
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Firm
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.attorneyInfo.currentAttorneyForIncarceratedPerson?.firm}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Address
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.attorneyInfo.currentAttorneyForIncarceratedPerson?.address}
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', gap: 6, mb: 3 }}>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Phone
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.attorneyInfo.currentAttorneyForIncarceratedPerson?.phone}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Email
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.attorneyInfo.currentAttorneyForIncarceratedPerson?.email}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Present at Hearing
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.attorneyInfo.currentAttorneyForIncarceratedPerson?.presentAtHearing
                  ? "Yes"
                  : "No"}
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', gap: 6, mb: 3 }}>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Representation Context
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.attorneyInfo.currentAttorneyForIncarceratedPerson?.representationContext}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: "left" }}>
                Trial Attorney
              </Typography>
              <Typography sx={{ color: "#1a1a1a", textAlign: "left" }}>
                {selectedData?.demographics.attorneyInfo.trialAttorney?.name}
              </Typography>
            </Box>
            <Box sx={{ flex: 1, minWidth: 200 }}>
              <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: 'left' }}>Appellate Attorney</Typography>
              <Typography sx={{ color: '#1a1a1a', textAlign: 'left' }}>{selectedData?.demographics.attorneyInfo.appellateAttorney?.name}</Typography>
            </Box>
          </Box>
          {Array.isArray(selectedData?.demographics.attorneyInfo?.otherLegalRepresentation) && selectedData.demographics.attorneyInfo.otherLegalRepresentation.length > 0 && (
            <Box sx={{ display: 'flex', gap: 6, mb: 3 }}>
              <Box sx={{ flex: 1, minWidth: 200 }}>
                <Typography variant="subtitle2" fontWeight={600} color="#6b7280" sx={{ mb: 0.5, textAlign: 'left' }}>Other Legal Representation</Typography>
                <Box>
                  {selectedData.demographics.attorneyInfo.otherLegalRepresentation.map((rep, idx) => (
                    <Typography key={idx} sx={{ color: '#1a1a1a', textAlign: 'left' }}>{rep.name} {rep.role ? `(${rep.role})` : ''} {'organization' in rep && rep.organization ? `- ${rep.organization}` : ''}</Typography>
                  ))}
                </Box>
              </Box>
              <Box sx={{ flex: 1, minWidth: 200 }} />
              <Box sx={{ flex: 1, minWidth: 200 }} />
            </Box>
          )}
          <Divider sx={{ mb: 3 }} />
          {/* New Evidence */}
          <Typography variant="h6" fontWeight={700} sx={{ mb: 1.5, color: '#1a1a1a', textAlign: 'left' }}>
            Additional Information
          </Typography>
          <ul style={{ marginBottom: 24, marginTop: 0, paddingLeft: 24, textAlign: "left" }}>
            {selectedData?.demographics.newEvidence.map((evidence, idx) => (
              <li key={idx} style={{ marginBottom: 8 }}>
                {evidence}
              </li>
            ))}
          </ul>
          <Divider sx={{ mb: 3 }} />
          {/* Physical Description */}
          <Typography variant="h6" fontWeight={700} sx={{ mb: 1.5, color: "#1a1a1a", textAlign: "left" }}>
            Physical Description
          </Typography>
          <ul style={{ marginBottom: 24, marginTop: 0, paddingLeft: 24, textAlign: "left" }}>
            <li style={{ marginBottom: 8 }}>Height: {selectedData?.demographics.physicalDescription.height}</li>
            <li style={{ marginBottom: 8 }}>Weight: {selectedData?.demographics.physicalDescription.weight}</li>
            <li style={{ marginBottom: 8 }}>Race: {selectedData?.demographics.physicalDescription.race}</li>
            <li style={{ marginBottom: 8 }}>Build: {selectedData?.demographics.physicalDescription.build}</li>
            <li style={{ marginBottom: 8 }}>
              Distinguishing Marks: {selectedData?.demographics.physicalDescription.distinguishingMarks}
            </li>
          </ul>
          <Divider sx={{ mb: 3 }} />
          {/* Victim Info */}
          <Typography variant="h6" fontWeight={700} sx={{ mb: 1.5, color: "#1a1a1a", textAlign: "left" }}>
            Victim Information
          </Typography>
          <ul style={{ marginBottom: 24, marginTop: 0, paddingLeft: 24, textAlign: "left" }}>
            <li style={{ marginBottom: 8 }}>Name: {selectedData?.demographics.victimInfo.name}</li>
            <li style={{ marginBottom: 8 }}>Relationship: {selectedData?.demographics.victimInfo.relationship}</li>
          </ul>
          <Divider sx={{ mb: 3 }} />
          {/* Prison Record */}
          <Typography variant="h6" fontWeight={700} sx={{ mb: 1.5, color: "#1a1a1a", textAlign: "left" }}>
            Prison Record
          </Typography>
          <ul style={{ marginBottom: 24, marginTop: 0, paddingLeft: 24, textAlign: "left" }}>
            <li style={{ marginBottom: 8 }}>Conduct: {selectedData?.demographics.prisonRecord.conduct}</li>
            <li style={{ marginBottom: 8 }}>Programming: {selectedData?.demographics.prisonRecord.programming}</li>
            <li style={{ marginBottom: 8 }}>Support: {selectedData?.demographics.prisonRecord.support}</li>
          </ul>
        </Paper>

        {/* Innocence Claim Modal */}
        <Modal open={isInnocenceModalOpen} onClose={() => setIsInnocenceModalOpen(false)}>
          <Box sx={{ bgcolor: '#fff', p: 4, borderRadius: 2, maxWidth: 600, mx: 'auto', my: 8, boxShadow: 3, outline: 'none', maxHeight: '70vh', overflowY: 'auto' }}>
            <Typography variant="h6" fontWeight={700} sx={{ mb: 2 }}>Possible Innocence Claims</Typography>
            {(innocenceFindings as Array<{
  quote: string;
  page: number;
  line: number;
  speaker: string;
  category: string;
  significance: string;
}>).map((finding, idx) => (
              <Paper key={idx} sx={{ p: 2, mb: 2, bgcolor: '#f7f8fa' }}>
                <Typography variant="subtitle2" fontWeight={700} sx={{ mb: 1 }}>
                  "{finding.quote}" ({finding.page},{finding.line})
                </Typography>
                <Typography variant="body2" sx={{ mb: 0.5 }}><b>Speaker:</b> {formatSpeakerName(finding.speaker)}</Typography>
                <Typography variant="body2" sx={{ mb: 0.5 }}><b>Category:</b> {formatCategory(finding.category)}</Typography>
                <Typography variant="body2"><b>Significance:</b> {finding.significance}</Typography>
              </Paper>
            ))}
            <Button variant="contained" color="primary" onClick={() => setIsInnocenceModalOpen(false)} sx={{ mt: 2 }}>Close</Button>
          </Box>
        </Modal>
      </Box>

      {/* PDF Upload Modal */}
      <PdfUploadModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} onUpload={handleNewUpload} />
    </Box>
  );
}

export default Dashboard;
