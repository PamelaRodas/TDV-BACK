const mongoose = require('mongoose');

const homeSchema = new mongoose.Schema(
  {
    title: {
      type: String,
      default: 'Manifestation Journal',
    },
    subtitle: {
      type: String,
      default: 'Tu espacio para rituales, intenciones y crecimiento personal',
    },
    description: {
      type: String,
      default: 'Un diario sagrado donde tus intenciones cobran vida. Registra rituales, manifestaciones y observa tu crecimiento energético.',
    },
    heroImage: {
      type: String,
      default: null,
    },
    tagline: {
      type: String,
      default: 'Manifiesta tu realidad, cultiva tu energía',
    },
    isActive: {
      type: Boolean,
      default: true,
    },
    createdAt: {
      type: Date,
      default: Date.now,
    },
  },
  { timestamps: true }
);

module.exports = mongoose.model('Home', homeSchema);
