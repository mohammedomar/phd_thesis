function T = AbruptBarrier(E,V1,V2,theta)
%AbruptBarrier transmission coefficient across an abrupt graphene PN junction.
% T = AbruptBarrier(E,V1,V2,theta) returns the transmission coefficient for
% a charge carrier with energy E incident from potential V1 to potential V2
% with an angle of incidence theta. The angle theta should lie between
% -pi/2 to pi/2 (incidence from left to right). In case of total internal
% reflection and the formation of evanescent waves no transmission is
% assumed, i.e. T=0 in case of Total Internal Reflection (TIR).

%Calculate the transmission coefficient

T = zeros(length(E),length(theta));

for i = 1:length(E)
    if V1 == V2
        T(i,:) = ones(size(T(i,:)));
    else
        %Reducing computations to enhance speed
        sinTheta = sin(theta);
        cosTheta = cos(theta);
        %     sinPhi = ((E(i)-V1).*sin(theta)./(E(i)-V2));
        sinPhi = ((E(i)-V1).*sinTheta./(E(i)-V2));
        cosPhi = sqrt(1-(sinPhi.^2));
        ind = sinPhi.^2 < 1; %Angles without TIR
        %     T(i,ind) = 2.*cos(theta(ind)).*cosPhi(ind);
        T(i,ind) = 2.*cosTheta(ind).*cosPhi(ind);
        %     T(i,ind) = T(i,(ind))./(1+(cos(theta(ind)).*cosPhi(ind))-(sinPhi(ind).*sin(theta(ind))));
        T(i,ind) = T(i,(ind))./(1+(cosTheta(ind).*cosPhi(ind))-(sinPhi(ind).*sinTheta(ind)));
    end
end