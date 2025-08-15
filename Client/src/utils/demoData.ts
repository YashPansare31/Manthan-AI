export const sampleAnalysisResults = {
  transcript: `Welcome everyone to today's quarterly planning meeting. I'm Sarah from the product team, and we have John from engineering, Lisa from marketing, and Mike from sales with us today.

Let's start with our Q4 objectives. John, can you give us an update on the technical infrastructure improvements?

John: Sure, Sarah. We've made significant progress on the server optimization project. We've reduced load times by 40% and improved database query performance. However, we're facing some challenges with the new authentication system. We need at least two more weeks to complete the security audit.

That sounds good, John. Lisa, what about the marketing campaign for our new feature launch?

Lisa: The campaign is on track. We've prepared social media content, email sequences, and partnership collaborations. Our target is to reach 50,000 new users in the first month. The creative assets are 90% complete, and we're planning to start the campaign next Monday.

Excellent. Mike, how are the Q3 sales numbers looking?

Mike: We've exceeded our Q3 targets by 15%. The new pricing strategy is working well. However, we're seeing increased competition in the enterprise segment. I recommend we consider a discount strategy for annual contracts to maintain our competitive edge.

Thanks Mike. Based on everyone's updates, I think we need to make some decisions. First, we need to prioritize the authentication system completion. Second, we should approve the discount strategy for enterprise customers. Third, we need to allocate additional budget for marketing given the strong Q3 performance.

John: I agree on the authentication priority. We can delay the mobile app optimization by one sprint to focus on security.

Lisa: The marketing team is ready to scale up if we get additional budget approval.

Mike: The discount strategy should help us secure more enterprise deals. I suggest a 20% discount for two-year contracts.

Perfect. Let's move forward with these decisions. Our next meeting is scheduled for next Friday to review progress. Thanks everyone for the productive discussion.`,

  summary: `This quarterly planning meeting covered three main areas: technical infrastructure, marketing campaigns, and sales performance. The engineering team reported 40% improvement in load times but needs two additional weeks for authentication system security audit. Marketing is ready to launch a new feature campaign targeting 50,000 new users, with creative assets 90% complete. Sales exceeded Q3 targets by 15% but faces increased enterprise competition. Key decisions include prioritizing authentication system completion, implementing a 20% discount strategy for two-year enterprise contracts, and increasing marketing budget allocation. The team agreed to delay mobile app optimization to focus on security priorities, with a follow-up meeting scheduled for next Friday.`,

  action_items: [
    "Complete security audit for authentication system within 2 weeks",
    "Launch marketing campaign for new feature next Monday",
    "Implement 20% discount strategy for two-year enterprise contracts",
    "Allocate additional budget for marketing team scaling",
    "Delay mobile app optimization by one sprint",
    "Schedule follow-up meeting for next Friday",
    "Prepare creative assets completion (remaining 10%)",
    "Finalize partnership collaboration agreements"
  ],

  key_decisions: [
    "Prioritize authentication system completion over mobile app optimization",
    "Approve 20% discount strategy for two-year enterprise contracts",
    "Increase marketing budget allocation based on Q3 performance",
    "Proceed with new feature campaign launch next Monday",
    "Delay mobile app optimization sprint to focus on security",
    "Target 50,000 new users in first month of campaign"
  ],

  processing_time: 42.7
};

export const generateRandomResults = () => {
  const variations = {
    transcript: [
      "Today's sprint retrospective focused on team velocity and process improvements...",
      "The client presentation went well, with several key stakeholders expressing interest...",
      "Our product roadmap discussion covered the next three quarters of development...",
      "The security review meeting identified several areas for immediate attention..."
    ],
    summary: [
      "Sprint retrospective revealed need for better communication tools and process refinement.",
      "Client presentation successful with follow-up actions identified for next quarter.",
      "Product roadmap aligned with business objectives and resource constraints.",
      "Security review highlighted critical vulnerabilities requiring immediate attention."
    ],
    action_items: [
      ["Implement new communication tools", "Schedule daily standups", "Review sprint velocity metrics"],
      ["Send follow-up proposal to client", "Prepare technical specifications", "Schedule demo session"],
      ["Finalize Q1 roadmap", "Allocate development resources", "Update stakeholder timelines"],
      ["Patch critical vulnerabilities", "Update security protocols", "Schedule penetration testing"]
    ],
    key_decisions: [
      ["Adopt new project management tool", "Increase sprint duration to 2 weeks"],
      ["Accept client requirements", "Adjust project timeline accordingly"],
      ["Prioritize mobile development", "Delay desktop feature updates"],
      ["Implement zero-trust security model", "Require multi-factor authentication"]
    ]
  };

  const randomIndex = Math.floor(Math.random() * variations.transcript.length);
  
  return {
    transcript: variations.transcript[randomIndex],
    summary: variations.summary[randomIndex],
    action_items: variations.action_items[randomIndex],
    key_decisions: variations.key_decisions[randomIndex],
    processing_time: Math.random() * 60 + 20 // 20-80 seconds
  };
};