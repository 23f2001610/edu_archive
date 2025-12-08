# Design Guidelines: Academic Resource Portal

## Design Approach
**System Selected**: Material Design + GitHub-inspired file browsing
**Rationale**: Educational portal requiring clear information hierarchy, efficient navigation, and reliable document access patterns. Function over form.

## Design Principles
1. **Clarity First**: Students must find resources in under 3 clicks
2. **Information Density**: Maximize useful content, minimize decoration
3. **Academic Professionalism**: Trustworthy, institutional aesthetic
4. **Responsive Efficiency**: Mobile students accessing on-the-go

## Typography
- **Primary Font**: Inter or Roboto (Google Fonts)
- **Headings**: 
  - H1: 2.5rem (font-semibold) - Page titles
  - H2: 1.875rem (font-semibold) - Section headers
  - H3: 1.5rem (font-medium) - Card/list headers
- **Body**: 1rem (font-normal) - All content text
- **Small**: 0.875rem - Metadata, timestamps, file sizes

## Layout System
**Spacing Units**: Tailwind 2, 4, 6, 8, 12, 16
- Cards/Components: p-4 to p-6
- Sections: py-8 to py-16
- Page margins: px-4 on mobile, px-8 on desktop

## Core Components

### Header Navigation
- Simple horizontal bar with logo/college name (left)
- Navigation links: Home | Notes | Question Papers | (Admin button if logged in)
- Login/Logout button (right)
- Sticky position for easy access
- Height: h-16

### Student View - Browse Interface
**Notes Section**:
- Course cards in grid: grid-cols-1 md:grid-cols-2 lg:grid-cols-3
- Each card shows: Course name, subject count, last updated
- Click card → list of subjects with file count
- Subject list → expandable file list with download buttons

**Question Papers Section**:
- Filter bar: Semester dropdown + Year dropdown
- Table/list view showing: Paper title, semester, year, upload date, download button
- Sortable columns

**File List Pattern** (GitHub-style):
- List items with: File icon, filename, file size, upload date, download icon-button
- Hover state reveals full metadata
- Clear visual separation between items

### Admin Dashboard
- Separate `/admin` route with distinct header indicator
- Side navigation: Dashboard | Manage Notes | Manage Question Papers | Upload
- Dashboard shows: Total files, recent uploads, quick actions
- CRUD tables with: Edit icon-button, Delete icon-button per row
- Upload forms with: Drag-drop zone, course/subject selectors, file input

### Forms
- Upload Form: Large drag-drop zone (border-dashed), file type indicator, progress bar
- Edit Form: Pre-filled inputs, clear save/cancel buttons
- Dropdowns for course/subject/semester selection
- Input fields: Consistent border, focus ring, label above

### Buttons
- Primary: Solid background, medium weight
- Secondary: Outlined with border
- Icon buttons: Minimal padding, hover background
- Download buttons: Icon + text combination

### Cards
- Border with subtle shadow
- Padding: p-6
- Hover: Slight shadow increase (no transform)
- Metadata in smaller text at bottom

## Navigation Patterns
- Breadcrumbs: Home > Notes > Computer Science > Subject Name
- Back buttons where applicable
- Clear "Back to [Section]" links

## Data Display
- Tables for admin management: Striped rows, hover highlight
- List view for students: Card-based for mobile, table for desktop
- File metadata always visible: Size, date, type icon

## Images
**No hero images required** - This is a functional portal, not marketing.
**File type icons**: Use Font Awesome for PDF, DOC, PPT recognition
**College logo**: Top-left header (max height: 40px)

## Authentication UI
- Simple centered login card (max-w-md)
- Username + Password fields
- "Login as Admin" button
- No registration - admin credentials pre-configured

## Admin Indicators
- Badge/pill showing "Admin Mode" in header
- Distinct accent for admin-only actions
- Confirmation modals for delete operations

## Accessibility
- Semantic HTML for document structure
- ARIA labels on icon-only buttons
- Keyboard navigation for all interactive elements
- Focus indicators on all inputs

## Performance Considerations
- Lazy load file lists (paginate if >50 items)
- Thumbnail generation for preview (future enhancement)
- No heavy animations - instant state changes preferred