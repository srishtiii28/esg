// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";

/**
 * @title ESGRegistry
 * @dev Contract for storing ESG report hashes and metadata on EduChain
 */
contract ESGRegistry is Ownable {
    struct Report {
        bytes32 reportHash;      // Hash of the ESG report
        uint256 timestamp;       // When the report was submitted
        string companyName;      // Name of the company
        string reportType;       // Type of ESG report (e.g., "Annual", "Quarterly")
        string ipfsHash;         // IPFS hash of the report (optional)
        bool verified;           // Whether the report is verified
    }

    // Mapping from report ID to Report struct
    mapping(bytes32 => Report) public reports;
    
    //Mapping from company name to their report IDs
    mapping(string => bytes32[]) public companyReports;

    // Events
    event ReportRegistered(
        bytes32 indexed reportId,
        bytes32 reportHash,
        string companyName,
        uint256 timestamp
    );

    event ReportVerified(
        bytes32 indexed reportId,
        address verifier
    );

    constructor() Ownable(msg.sender) {}

    /**
     * @dev Register a new ESG report
     * @param reportHash Hash of the ESG report
     * @param companyName Name of the company
     * @param reportType Type of the report
     * @param ipfsHash IPFS hash of the report (optional)
     */
    function registerReport(
        bytes32 reportHash,
        string memory companyName,
        string memory reportType,
        string memory ipfsHash
    ) public returns (bytes32) {
        require(bytes(companyName).length > 0, "Company name cannot be empty");
        
        // Generate a unique report ID using company name, timestamp, and report hash
        bytes32 reportId = keccak256(
            abi.encodePacked(
                companyName,
                block.timestamp,
                reportHash
            )
        );

        // Ensure report hasn't been registered before
        require(reports[reportId].timestamp == 0, "Report already registered");

        // Create and store the report
        Report memory newReport = Report({
            reportHash: reportHash,
            timestamp: block.timestamp,
            companyName: companyName,
            reportType: reportType,
            ipfsHash: ipfsHash,
            verified: false
        });

        reports[reportId] = newReport;
        companyReports[companyName].push(reportId);

        emit ReportRegistered(reportId, reportHash, companyName, block.timestamp);
        
        return reportId;
    }

    /**
     * @dev Verify a report (only owner can verify)
     * @param reportId ID of the report to verify
     */
    function verifyReport(bytes32 reportId) public onlyOwner {
        require(reports[reportId].timestamp > 0, "Report does not exist");
        require(!reports[reportId].verified, "Report already verified");

        reports[reportId].verified = true;
        emit ReportVerified(reportId, msg.sender);
    }

    /**
     * @dev Get report details
     * @param reportId ID of the report
     */
    function getReport(bytes32 reportId) public view returns (
        bytes32 reportHash,
        uint256 timestamp,
        string memory companyName,
        string memory reportType,
        string memory ipfsHash,
        bool verified
    ) {
        Report memory report = reports[reportId];
        require(report.timestamp > 0, "Report does not exist");
        
        return (
            report.reportHash,
            report.timestamp,
            report.companyName,
            report.reportType,
            report.ipfsHash,
            report.verified
        );
    }

    /**
     * @dev Get all reports for a company
     * @param companyName Name of the company
     */
    function getCompanyReports(string memory companyName) 
        public 
        view 
        returns (bytes32[] memory) 
    {
        return companyReports[companyName];
    }

    /**
     * @dev Verify if a report hash matches the stored hash
     * @param reportId ID of the report
     * @param hash Hash to verify against
     */
    function verifyHash(bytes32 reportId, bytes32 hash) public view returns (bool) {
        require(reports[reportId].timestamp > 0, "Report does not exist");
        return reports[reportId].reportHash == hash;
    }
}
