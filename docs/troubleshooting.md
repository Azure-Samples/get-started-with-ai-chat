# Troubleshooting Guide

This guide provides solutions to common issues you may encounter when deploying and running the application.

## Provisioning and Deployment Failures

### Resource Provisioning Issues

**Problem**: Timeouts or provisioning resources fail
**Solution**: 
- Change the location of your resource group, as there may be availability constraints for resources
- Call `azd down` and remove your current resources
- Delete the `.azure` folder from your workspace
- Call `azd up` again and select a different region

### Debugging Deployment Issues

**Debug Commands**:
- Use `azd show` to display information about your app and resources
- Use `azd deploy --debug` to enable debugging and logging while deploying the application's code to Azure

**General Checks**:
- Ensure that your `az` and `azd` tools are up to date
- After fully deploying with azd, additional errors in the Azure Portal may indicate that your latest code has not been successfully deployed

## Azure Container Apps

### Container App Boot Issues

**Problem**: ACA does not boot up
**Possible Causes**: Deployment failure due to quota constraints, permission issues, or resource availability
**Solution**: Check failures in the deployment and container app logs in the Azure Portal

### Logging and Debugging

**Console Traces**: 
- Can be found in the Azure Portal, but they may be unreliable
- Use Python's logging with INFO level
- Adjust Azure HTTP logging to WARNING

**Frontend Debugging**:
- Once your ACA is deployed, utilize the browser debugger (F12)
- Clear cache (CTRL+SHIFT+R) to help debug the frontend for better traceability

## Getting Help

If you continue to experience issues after trying these solutions:

1. Check the [Microsoft Foundry documentation](https://learn.microsoft.com/azure/ai-foundry/)
2. Review the [Azure Container Apps troubleshooting guide](https://learn.microsoft.com/azure/container-apps/troubleshooting)
3. Consult the [Azure Developer CLI reference](https://learn.microsoft.com/azure/developer/azure-developer-cli/reference)
