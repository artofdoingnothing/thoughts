import { jsPDF } from 'jspdf';
import type { Conversation, Message } from '../types';

const LEGEND_COLORS = ['#4A90D9', '#E07B3A', '#6DB87A', '#A063C6', '#D95F5F', '#4ABFBF'];

function renderRichParagraph(
  doc: jsPDF,
  text: string,
  startX: number,
  startY: number,
  maxWidth: number,
  isCodeBlock: boolean,
  isQuote: boolean,
  lineHeightMm: number,
  margins: any,
  quoteColor: string
): number {
  let currentX = startX;
  let currentY = startY;
  const bottomY = doc.internal.pageSize.getHeight() - margins.bottom;

  if (isCodeBlock) {
    doc.setFont('courier', 'normal');
    doc.setFontSize(7.5);
    doc.setTextColor('#2C2C2C');
    const lines = doc.splitTextToSize(text, maxWidth);
    const blockHeight = lines.length * lineHeightMm + 2;

    if (currentY + blockHeight > bottomY) {
      doc.addPage();
      currentY = margins.top;
    }

    doc.setFillColor('#F4F4F4');
    doc.setDrawColor('#DEDEDE');
    doc.setLineWidth(0.35);
    doc.rect(startX, currentY - 3.5, maxWidth + 4, blockHeight, 'FD');

    for (const line of lines) {
      doc.text(line, startX + 2, currentY);
      currentY += lineHeightMm;
    }
    return currentY;
  }

  const defaultFont = 'helvetica';
  const defaultStyle = isQuote ? 'italic' : 'normal';
  const defaultSize = isQuote ? 7.5 : 9;
  const defaultColor = isQuote ? '#7A7A7A' : '#3A3A3A';

  const tokens = text.split(/`/g);
  let startQuoteY = currentY;

  for (let i = 0; i < tokens.length; i++) {
    const isCodeSpan = i % 2 !== 0; // Odd indexes are code inside backticks
    if (!tokens[i]) continue;

    const words = tokens[i].split(' ');
    for (let j = 0; j < words.length; j++) {
      const w = words[j];
      const hasSpace = j < words.length - 1;
      const wordWithSpace = w + (hasSpace ? ' ' : '');

      if (isCodeSpan) {
        doc.setFont('courier', 'normal');
        doc.setFontSize(8);
        doc.setTextColor('#C0392B');
      } else {
        doc.setFont(defaultFont, defaultStyle);
        doc.setFontSize(defaultSize);
        doc.setTextColor(defaultColor);
      }

      const wWidth = doc.getTextWidth(wordWithSpace);
      if (currentX + doc.getTextWidth(w) > startX + maxWidth && currentX > startX) {
        // Wrap to next line
        currentY += lineHeightMm;
        currentX = startX;
        if (currentY > bottomY) {
          // If we break a quote across a page, we draw the first half of the line
          if (isQuote) {
            doc.setDrawColor(quoteColor);
            doc.setLineWidth(0.5); // 1.5pt
            doc.line(startX - 2.5, startQuoteY - 2.5, startX - 2.5, currentY - lineHeightMm + 1);
          }
          doc.addPage();
          currentY = margins.top;
          startQuoteY = margins.top; // reset quote top for the new page
        }
      }

      if (isCodeSpan && w.length > 0) {
        const cleanWidth = doc.getTextWidth(w);
        doc.setFillColor('#F7F7F7');
        doc.setDrawColor('#E8E8E8');
        doc.setLineWidth(0.35); // 1px
        doc.rect(currentX, currentY - 2.5, cleanWidth + 1, 3.5, 'FD');
        doc.text(w, currentX + 0.5, currentY);
      } else if (w.length > 0) {
        doc.text(w, currentX, currentY);
      }

      currentX += wWidth;
    }
  }

  if (isQuote) {
    doc.setDrawColor(quoteColor);
    doc.setLineWidth(0.5); // 1.5pt
    doc.line(startX - 2.5, startQuoteY - 2.5, startX - 2.5, currentY + 1);
  }

  return currentY;
}

export const generateConversationPdf = (conversation: Conversation) => {
  // A4 size: 210 × 297mm
  const doc = new jsPDF({
    orientation: 'portrait',
    unit: 'mm',
    format: 'a4'
  });

  const margins = { top: 16, bottom: 20, left: 14, right: 14 }; // Increased bottom margin for footer
  const pageWidth = doc.internal.pageSize.getWidth();
  const maxWidth = pageWidth - margins.left - margins.right;
  let yPosition = margins.top;

  // Title: 18pt bold, #1A1A1A
  doc.setFontSize(18);
  doc.setFont('helvetica', 'bold');
  doc.setTextColor('#1A1A1A');
  const titleLines = doc.splitTextToSize(conversation.title, maxWidth);
  doc.text(titleLines, margins.left, yPosition);
  yPosition += titleLines.length * 8;

  // Context: 9pt regular, #6B6B6B
  doc.setFontSize(9);
  doc.setFont('helvetica', 'normal');
  doc.setTextColor('#6B6B6B');
  const contextLines = doc.splitTextToSize(conversation.context || 'No context provided.', maxWidth);
  doc.text(contextLines, margins.left, yPosition);
  yPosition += contextLines.length * 4.5 + 2;

  // Metadata row: 8pt #9E9E9E
  doc.setFontSize(8);
  doc.setTextColor('#9E9E9E');
  const dateStr = `Exported on: ${new Date().toLocaleString()}`;
  doc.text(dateStr, margins.left, yPosition);

  const participantCount = conversation.personas?.length || 0;
  const partCountStr = `${participantCount} Participant${participantCount !== 1 ? 's' : ''}`;
  doc.text(partCountStr, pageWidth - margins.right, yPosition, { align: 'right' });

  yPosition += 6;

  // Separator: 1px rule #E0E0E0
  doc.setLineWidth(0.35);
  doc.setDrawColor('#E0E0E0');
  doc.line(margins.left, yPosition, pageWidth - margins.right, yPosition);

  yPosition += 8;

  // Participant Legend
  const personaColors = new Map<number, string>();
  if (conversation.personas && conversation.personas.length > 0) {
    let currentX = margins.left;
    const dotRadius = 1.4;

    doc.setFontSize(8);
    doc.setFont('helvetica', 'normal');

    conversation.personas.forEach((p, i) => {
      const color = LEGEND_COLORS[i % LEGEND_COLORS.length];
      personaColors.set(p.id, color);

      const text = p.name;
      const textWidth = doc.getTextWidth(text);
      const itemWidth = (dotRadius * 2) + 2 + textWidth + 8;

      if (currentX + itemWidth - 8 > pageWidth - margins.right) {
        currentX = margins.left;
        yPosition += 6;
      }

      doc.setFillColor(color);
      doc.circle(currentX + dotRadius, yPosition - 1, dotRadius, 'F');

      doc.setTextColor('#444444');
      doc.text(text, currentX + (dotRadius * 2) + 2, yPosition);

      currentX += itemWidth;
    });

    yPosition += 10;
  }

  // Messages
  const messages = [...conversation.messages].sort(
    (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
  );

  let prevMsg: Message | null = null;
  const bodyIndent = 5;
  const dotRadius = 1.25;
  const lineHeightMm = 9 * 1.4 * 0.352778; // ~4.44 mm

  for (const msg of messages) {
    const currentMsgDate = new Date(msg.created_at);
    const prevMsgDate = prevMsg ? new Date(prevMsg.created_at) : null;

    const isSameSender = prevMsg ? prevMsg.persona_id === msg.persona_id : false;
    const timeDiffMinutes = prevMsgDate ? (currentMsgDate.getTime() - prevMsgDate.getTime()) / 60000 : Infinity;
    const isWithin5Mins = timeDiffMinutes <= 5;

    // Cross-day jump timestamp
    const currentMsgDateStr = currentMsgDate.toDateString();
    const prevMsgDateStr = prevMsgDate ? prevMsgDate.toDateString() : null;

    if (currentMsgDateStr !== prevMsgDateStr) {
      if (prevMsg) yPosition += 6;

      if (yPosition + 8 > doc.internal.pageSize.getHeight() - margins.bottom) {
        doc.addPage();
        yPosition = margins.top;
      }

      doc.setFontSize(7.5);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor('#AAAAAA');

      const dayStr = currentMsgDate.toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' });
      const text = `— ${dayStr} —`;
      const textWidth = doc.getTextWidth(text);
      const centerX = (pageWidth - textWidth) / 2;

      doc.text(text, centerX, yPosition);
      yPosition += 8;

      // Force a full header row after a day jump regardless of time difference
    } else if (prevMsg) {
      const gap = isSameSender ? 0.7 : 1.41;
      yPosition += gap;
    }

    if (yPosition + 8 > doc.internal.pageSize.getHeight() - margins.bottom) {
      doc.addPage();
      yPosition = margins.top;
    }

    const forcedHeader = currentMsgDateStr !== prevMsgDateStr;
    const pColor = personaColors.get(msg.persona_id) || '#000000';

    if (!forcedHeader && isSameSender && isWithin5Mins) {
      // Omit sender name, flow immediately.
    } else if (!forcedHeader && isSameSender && !isWithin5Mins) {
      doc.setFontSize(7.5);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor('#AAAAAA');
      const timeStr = currentMsgDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      doc.text(timeStr, pageWidth - margins.right, yPosition, { align: 'right' });
      yPosition += 3.5;
    } else {
      doc.setFillColor(pColor);
      doc.circle(margins.left + dotRadius, yPosition - 1, dotRadius, 'F');

      const senderName = msg.persona?.name || 'Unknown';
      doc.setFontSize(8);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor('#2C2C2C');
      const nameX = margins.left + bodyIndent;
      doc.text(senderName, nameX, yPosition);

      const nameWidth = doc.getTextWidth(senderName);
      doc.setFontSize(7.5);
      doc.setFont('helvetica', 'normal');
      doc.setTextColor('#AAAAAA');
      const timeStr = currentMsgDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      doc.text(timeStr, nameX + nameWidth + 2, yPosition);

      yPosition += lineHeightMm;
    }

    // Advanced block parsing
    const rawBlocks = msg.content.split('\n');
    let inCodeBlock = false;
    let codeBlockContent: string[] = [];

    const flushCodeBlock = () => {
      if (codeBlockContent.length > 0) {
        yPosition = renderRichParagraph(
          doc,
          codeBlockContent.join('\n'),
          margins.left + bodyIndent,
          yPosition + 2, // top margin
          maxWidth - bodyIndent - 4,
          true,
          false,
          lineHeightMm,
          margins,
          pColor
        );
        yPosition += lineHeightMm; // block margin
        codeBlockContent = [];
      }
    };

    for (let rawLine of rawBlocks) {
      // Code block toggler
      if (rawLine.startsWith('```')) {
        if (inCodeBlock) {
          flushCodeBlock();
          inCodeBlock = false;
        } else {
          inCodeBlock = true;
          codeBlockContent = [];
        }
        continue;
      }

      if (inCodeBlock) {
        codeBlockContent.push(rawLine);
        continue;
      }

      const isQuote = rawLine.startsWith('>');
      if (isQuote) {
        rawLine = rawLine.substring(1).trim();
      }

      const pMaxWidth = isQuote ? maxWidth - bodyIndent - 5 : maxWidth - bodyIndent;
      const startX = isQuote ? margins.left + bodyIndent + 5 : margins.left + bodyIndent;

      if (isQuote) yPosition += 1.4; // 4px padding for quotes

      yPosition = renderRichParagraph(
        doc,
        rawLine.length > 0 ? rawLine : ' ', // empty paragraph behavior
        startX,
        yPosition,
        pMaxWidth,
        false,
        isQuote,
        lineHeightMm,
        margins,
        pColor
      );

      // Paragraph spacing
      yPosition += isQuote ? 1.4 + lineHeightMm : lineHeightMm; 
    }

    // Flush any unclosed code blocks
    if (inCodeBlock) {
      flushCodeBlock();
    }

    prevMsg = msg;
  }

  // System Page Footer
  const pageCount = doc.getNumberOfPages();
  const footerTitle = conversation.title.length > 40 ? conversation.title.substring(0, 37) + '...' : conversation.title;

  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    const footerY = doc.internal.pageSize.getHeight() - 8;

    // Separation rule
    doc.setLineWidth(0.5 * 0.3528); // 0.5pt into mm
    doc.setDrawColor('#E8E8E8');
    doc.line(margins.left, footerY - 4, pageWidth - margins.right, footerY - 4);

    doc.setFontSize(8);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor('#BDBDBD');

    // Left title
    doc.text(footerTitle, margins.left, footerY);

    // Right Page X of Y
    const pageText = `Page ${i} of ${pageCount}`;
    doc.text(pageText, pageWidth - margins.right, footerY, { align: 'right' });
  }

  doc.save(`${conversation.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.pdf`);
};
