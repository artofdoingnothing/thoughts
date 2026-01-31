# Client Code Guidelines

## Technology Stack
- **Framework**: React
- **UI Library**: Material UI (MUI)
- **Styling**: Emotion (MUI default) or SCSS modules if necessary, but prefer MUI's `sx` prop or styled components.

## Color Palette

### CSS Variables
```css
:root {
  /* CSS HEX */
  --pale-oak: #dbcfb0ff;
  --ash-grey: #bfc8adff;
  --muted-teal: #90b494ff;
  --slate-grey: #718f94ff;
  --dusty-grape: #545775ff;

  /* CSS HSL */
  --pale-oak-hsl: hsla(43, 37%, 77%, 1);
  --ash-grey-hsl: hsla(80, 20%, 73%, 1);
  --muted-teal-hsl: hsla(127, 19%, 64%, 1);
  --slate-grey-hsl: hsla(189, 14%, 51%, 1);
  --dusty-grape-hsl: hsla(235, 16%, 39%, 1);
}
```

### SCSS Variables
```scss
/* SCSS HEX */
$pale-oak: #dbcfb0ff;
$ash-grey: #bfc8adff;
$muted-teal: #90b494ff;
$slate-grey: #718f94ff;
$dusty-grape: #545775ff;

/* SCSS HSL */
$pale-oak-hsl: hsla(43, 37%, 77%, 1);
$ash-grey-hsl: hsla(80, 20%, 73%, 1);
$muted-teal-hsl: hsla(127, 19%, 64%, 1);
$slate-grey-hsl: hsla(189, 14%, 51%, 1);
$dusty-grape-hsl: hsla(235, 16%, 39%, 1);

/* SCSS RGB */
$pale-oak-rgb: rgba(219, 207, 176, 1);
$ash-grey-rgb: rgba(191, 200, 173, 1);
$muted-teal-rgb: rgba(144, 180, 148, 1);
$slate-grey-rgb: rgba(113, 143, 148, 1);
$dusty-grape-rgb: rgba(84, 87, 117, 1);

/* Gradients */
$gradient-top: linear-gradient(0deg, #dbcfb0ff, #bfc8adff, #90b494ff, #718f94ff, #545775ff);
$gradient-right: linear-gradient(90deg, #dbcfb0ff, #bfc8adff, #90b494ff, #718f94ff, #545775ff);
$gradient-bottom: linear-gradient(180deg, #dbcfb0ff, #bfc8adff, #90b494ff, #718f94ff, #545775ff);
$gradient-left: linear-gradient(270deg, #dbcfb0ff, #bfc8adff, #90b494ff, #718f94ff, #545775ff);
$gradient-top-right: linear-gradient(45deg, #dbcfb0ff, #bfc8adff, #90b494ff, #718f94ff, #545775ff);
$gradient-bottom-right: linear-gradient(135deg, #dbcfb0ff, #bfc8adff, #90b494ff, #718f94ff, #545775ff);
$gradient-top-left: linear-gradient(225deg, #dbcfb0ff, #bfc8adff, #90b494ff, #718f94ff, #545775ff);
$gradient-bottom-left: linear-gradient(315deg, #dbcfb0ff, #bfc8adff, #90b494ff, #718f94ff, #545775ff);
$gradient-radial: radial-gradient(#dbcfb0ff, #bfc8adff, #90b494ff, #718f94ff, #545775ff);
```

## Aesthetic Guidelines
- **Visual Style**: Premium, modern, and dynamic.
- **Typography**: Modern fonts (e.g., Inter, Roboto, Outfit).
- **Interactions**: Use hover effects, subtle micro-animations, and smooth transitions.
- **Design System**: Strict adherence to the color palette and Material UI components.
