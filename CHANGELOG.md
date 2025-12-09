# Changelog

All notable changes to this project will be documented in this file.

## [0.1.14] - 2025-12-09
### Changed
- **Project structure in `README.md`**.

## [0.1.13] - 2025-12-09

### Fixed
- **RML Term Type Defaults**: Fixed `MappingParser._create_ext_expr()` to correctly apply R2RML default term types:
  - Subject Maps now default to `rr:IRI` (was incorrectly defaulting to Literal)
  - Predicate Maps now default to `rr:IRI` (was incorrectly defaulting to Literal)
  - Object Maps continue to default to `rr:Literal` (correct)
- This fix ensures generated RDF subjects and predicates are proper IRIs, not literals, making the output conformant with RDF standards

### Technical Details
- Modified `_create_ext_expr()` to accept `default_term_type` parameter
- Updated method calls in `parse()` to specify appropriate defaults based on map type