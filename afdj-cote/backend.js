// afdj-cote/backend.js - Node.js + Express + pdf-parse
import express from 'express';
import cors from 'cors';
import axios from 'axios';
import pdf from 'pdf-parse';
import cron from 'node-cron';

const app = express();
app.use(cors());
app.use(express.json());

const PDF_URL = 'https://www.afdj.ro/sites/default/files/bhcote.pdf';

async function parseAFDJ() {
  try
