const path = require("path");
const express = require("express");
require("dotenv").config();

const app = express();
const port = process.env.PORT || 3000;
const flaskSubmitUrl = process.env.FLASK_SUBMIT_URL;

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get("/", (_req, res) => {
  res.send("server is healthy!");
});

app.post("/submit", async (req, res) => {
  const {
    itemId = "",
    itemUUID = "",
    itemHash = "",
    itemName = "",
    itemDescription = "",
  } = req.body;

  if (!flaskSubmitUrl) {
    return res.status(500).render("form", {
      error: "FLASK_SUBMIT_URL is not set in environment.",
      success: null,
    });
  }

  if (!itemName.trim() || !itemDescription.trim()) {
    return res.status(400).render("form", {
      error: "Item Name and Item Description are required.",
      success: null,
    });
  }

  try {
    const response = await fetch(flaskSubmitUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        itemId: itemId.trim(),
        itemUUID: itemUUID.trim(),
        itemHash: itemHash.trim(),
        itemName: itemName.trim(),
        itemDescription: itemDescription.trim(),
      }),
    });

    const contentType = response.headers.get("content-type") || "";
    const responseBody = contentType.includes("application/json")
      ? await response.json()
      : await response.text();

    if (!response.ok) {
      const backendError =
        typeof responseBody === "object" && responseBody !== null
          ? responseBody.error
          : String(responseBody);

      return res.status(response.status).render("form", {
        error: backendError || "Backend request failed.",
        success: null,
      });
    }

    return res.render("form", {
      error: null,
      success: "Todo item submitted successfully.",
    });
  } catch (error) {
    return res.status(500).render("form", {
      error: error.message || "Failed to reach Flask backend.",
      success: null,
    });
  }
});

app.listen(port, () => {
  console.log(`Express frontend running on port: ${port}`);
});
