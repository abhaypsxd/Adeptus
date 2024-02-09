const express = require("express");
const mongoose = require("mongoose");
const multer = require("multer");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = 3000;

// Connect to MongoDB
mongoose
  .connect("mongodb://localhost:27017/pdfUploadDB", {
    useNewUrlParser: true,
    useUnifiedTopology: true,
  })
  .then(() => console.log("Connected to MongoDB"))
  .catch((err) => console.error("Error connecting to MongoDB:", err));

// Define schema
const pdfSchema = new mongoose.Schema({
  filename: String,
  contentType: String,
  data: Buffer,
});

const PDF = mongoose.model("PDF", pdfSchema);

// Set up multer for file uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "./uploads");
  },
  filename: function (req, file, cb) {
    cb(null, file.originalname);
  },
});

// Modify file filter to only accept PDF files
const fileFilter = (req, file, cb) => {
  if (file.mimetype === "application/pdf") {
    cb(null, true);
  } else {
    cb(new Error("Only PDF files are allowed"));
  }
};

const upload = multer({ storage: storage, fileFilter: fileFilter });

// Upload PDF
app.post("/upload", upload.single("pdf"), async (req, res) => {
  try {
    const pdf = new PDF({
      filename: req.file.originalname,
      contentType: req.file.mimetype,
      data: fs.readFileSync(
        path.join(__dirname, "/uploads/", req.file.filename)
      ),
    });
    await pdf.save();
    res.send("PDF uploaded successfully");
  } catch (error) {
    console.error(error);
    res.status(500).send("Internal Server Error");
  }
});

// Get PDF
app.get("/pdf/:filename", async (req, res) => {
  try {
    const pdf = await PDF.findOne({ filename: req.params.filename });
    if (!pdf) {
      return res.status(404).send("PDF not found");
    }
    res.set("Content-Type", pdf.contentType);
    res.send(pdf.data);
  } catch (error) {
    console.error(error);
    res.status(500).send("Internal Server Error");
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
