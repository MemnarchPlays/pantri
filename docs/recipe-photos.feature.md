---
name: Recipe Photos
description: Upload, store, display, and delete photos attached to individual recipes
flow: recipe.flow.md
status: COMPLETE
---

## What It Does

Allows users to attach one or more photos to any recipe. Photos are uploaded via the Add/Edit Recipe form, stored in `data/images/<slug>/`, and their relative paths are saved in the recipe JSON under a `photos` array. The recipe detail page renders all photos in a gallery section. Existing photos can be removed individually from the Edit form.

## Success Criteria

1. The Add Recipe and Edit Recipe forms include a "Add Photos" file input that accepts jpg, jpeg, png, gif, and webp files (multiple selection allowed).
2. On form submit, each uploaded image is saved to `data/images/<slug>/` using its sanitized original filename.
3. The recipe JSON gains a `photos` array of relative paths (e.g. `["data/images/pasta-bake/photo1.jpg"]`); recipes with no photos have no `photos` key (backward compatible).
4. The recipe detail page renders all photos in a gallery section above the ingredient list when `photos` is non-empty.
5. If a recipe has no photos, the detail page shows no photo section (no empty placeholder, no error).
6. On the Edit Recipe page, each existing photo is listed with a thumbnail and a "Remove" button.
7. Clicking "Remove" on an existing photo deletes the file from disk and removes its path from the JSON, without a full page reload (or with a page reload that keeps the form state).
8. Uploading a file with a non-image extension (e.g. `.pdf`, `.exe`) is rejected server-side with a `400` error; the form shows an error message.
9. If the recipe is renamed (slug changes), the images folder is renamed from the old slug to the new slug.
10. Deleting a recipe also deletes its `data/images/<slug>/` folder.

## Status

COMPLETE

### Progress

- [x] Update Add/Edit form templates to include file input for photos
- [x] Server-side upload handler: validate type, save to `data/images/<slug>/`, write paths to JSON
- [x] Serve uploaded images via a static route (`/recipe-images/<slug>/<filename>`)
- [x] Detail page: render photo gallery when `photos` present
- [x] Edit page: list existing photos with thumbnails and Remove buttons
- [x] Remove: JS removes hidden input from form; server deletes removed files on save
- [x] Rename handling: move image folder when slug changes
- [x] Delete recipe: remove image folder
- [x] Backward compatibility: load existing JSON files without `photos` key without error

## Scope

- Image upload, storage, display, and deletion for recipes
- Out of scope: image compression/resizing, CDN hosting, image reordering (drag-and-drop), caption text per photo

## Files

- `pantri/routes/recipes.py` — add/edit/delete route handlers (upload, remove, rename)
- `templates/` — add/edit recipe form templates, detail page template
- `data/images/` — uploaded image storage (gitignored)
- `docs/recipe.flow.md` — flow doc (updated to include photos steps)
