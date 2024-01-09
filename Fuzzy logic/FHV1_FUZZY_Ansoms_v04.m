function [outputMatrix] = FHV1_FUZZY_Ansoms_v04(inputMatrix)
    warning('off','all');
    % Load the FIS from a file
    fis = readfis('FHV1_FUZZY_Ansoms_v04.fis');
    
    % Determine the number of input vectors
    numberCallusElements = size(inputMatrix, 1);
    
    % Initialize the outputMatrix
    outputMatrix = zeros(numberCallusElements, 4);
    
    % Parallelize FIS evaluation (if you have the Parallel Computing Toolbox)
    parpool(8); % Create a parallel pool
    opt = evalfisOptions('NoRuleFiredMessage', "none", 'EmptyOutputFuzzySetMessage',"none");

    parfor i = 1:numberCallusElements
        outputMatrix(i, :) = evalfis(fis, inputMatrix(i, :), opt);
    end
    
    % If you're done with parallel computing, you can delete the parallel pool
    delete(gcp);
end