# Task Planning & Breakdown

## Description
Breaks down complex tasks into smaller, manageable subtasks with clear steps and dependencies. Helps organize work and create actionable plans.

## Category
Automation

## Input Parameters
- `task`: The main task or goal to break down (string)
- `complexity_level`: Expected complexity - "simple", "moderate", "complex" (optional, default: "moderate")
- `output_format`: Format of the plan - "checklist", "flowchart", "steps" (optional, default: "steps")

## Output
A structured breakdown of the task into:
- Individual subtasks
- Estimated time for each subtask
- Dependencies between tasks
- Priority/order recommendations

## Usage Example
```
Input:
  task: "Build a web application for task management"
  complexity_level: "complex"
  output_format: "steps"

Output:
  Phase 1: Planning & Design
  1. Define requirements (2 hours)
  2. Create wireframes (3 hours)
  3. Design database schema (2 hours)
  
  Phase 2: Backend Development (depends on Phase 1)
  4. Set up development environment (1 hour)
  5. Implement user authentication (4 hours)
  6. Create task CRUD operations (6 hours)
  7. Add API endpoints (4 hours)
  
  Phase 3: Frontend Development (depends on Phase 2)
  8. Create UI components (8 hours)
  9. Implement state management (4 hours)
  10. Connect to backend API (3 hours)
  
  Phase 4: Testing & Deployment (depends on Phase 3)
  11. Write tests (6 hours)
  12. Bug fixes (4 hours)
  13. Deploy to production (2 hours)
```

## Dependencies
- Task analysis capability
- Understanding of project management principles
- Knowledge of development workflows

## Notes
- Adjusts detail level based on task complexity
- Can incorporate industry best practices
- Useful for project management and planning
- Considers realistic time estimates
