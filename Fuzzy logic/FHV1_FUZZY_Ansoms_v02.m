function [outputMatrix] = FHV1_FUZZY_Ansoms_v02(inputMatrix)
    warning('off','all');
    newInputMatrix = [inputMatrix(:, 1:2), sum(inputMatrix(:, 3:4), 2), inputMatrix(:, 5:8)];
    outputMatrix = parfeval(evalfis(readfis('FHV1_FUZZY_Ansoms_v02.fis'), newInputMatrix));
end