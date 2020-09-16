
module soc(clk, stdout_ready_in, stdin_valid_in, stdin_data_in, stdout_valid_out, stdout_out, stdin_ready_out);
  input [0:0] stdout_ready_in;
  input [0:0] stdin_valid_in;
  input [31:0] stdin_data_in;
  input [0:0] clk;
  output [0:0] stdout_valid_out;
  output [31:0] stdout_out;
  output [0:0] stdin_ready_out;
  wire [0:0] exp_188;
  wire [0:0] exp_172;
  wire [0:0] exp_180;
  wire [0:0] exp_5;
  wire [0:0] exp_216;
  wire [0:0] exp_500;
  wire [0:0] exp_365;
  wire [6:0] exp_350;
  wire [31:0] exp_348;
  wire [31:0] exp_96;
  wire [31:0] exp_95;
  wire [23:0] exp_94;
  wire [15:0] exp_93;
  wire [7:0] exp_82;
  wire [0:0] exp_81;
  wire [0:0] exp_86;
  wire [9:0] exp_77;
  wire [29:0] exp_85;
  wire [31:0] exp_8;
  wire [31:0] exp_230;
  wire [32:0] exp_581;
  wire [0:0] exp_577;
  wire [0:0] exp_525;
  wire [0:0] exp_503;
  wire [0:0] exp_361;
  wire [6:0] exp_360;
  wire [0:0] exp_363;
  wire [6:0] exp_362;
  wire [0:0] exp_524;
  wire [0:0] exp_369;
  wire [6:0] exp_368;
  wire [0:0] exp_523;
  wire [0:0] exp_522;
  wire [0:0] exp_521;
  wire [2:0] exp_351;
  wire [0:0] exp_520;
  wire [0:0] exp_504;
  wire [31:0] exp_340;
  wire [31:0] exp_278;
  wire [0:0] exp_274;
  wire [4:0] exp_254;
  wire [0:0] exp_273;
  wire [0:0] exp_277;
  wire [31:0] exp_270;
  wire [0:0] exp_251;
  wire [0:0] exp_572;
  wire [0:0] exp_571;
  wire [0:0] exp_570;
  wire [0:0] exp_569;
  wire [4:0] exp_233;
  wire [4:0] exp_564;
  wire [0:0] exp_407;
  wire [0:0] exp_406;
  wire [0:0] exp_405;
  wire [0:0] exp_404;
  wire [0:0] exp_403;
  wire [0:0] exp_402;
  wire [0:0] exp_353;
  wire [4:0] exp_352;
  wire [0:0] exp_355;
  wire [5:0] exp_354;
  wire [0:0] exp_357;
  wire [5:0] exp_356;
  wire [0:0] exp_359;
  wire [4:0] exp_358;
  wire [0:0] exp_228;
  wire [0:0] exp_227;
  wire [0:0] exp_225;
  wire [0:0] exp_224;
  wire [0:0] exp_222;
  wire [0:0] exp_223;
  wire [0:0] exp_221;
  wire [0:0] exp_582;
  wire [0:0] exp_220;
  wire [0:0] exp_219;
  wire [0:0] exp_586;
  wire [0:0] exp_585;
  wire [0:0] exp_584;
  wire [0:0] exp_583;
  wire [0:0] exp_215;
  wire [0:0] exp_206;
  wire [0:0] exp_201;
  wire [0:0] exp_198;
  wire [31:0] exp_1;
  wire [31:0] exp_212;
  wire [31:0] exp_419;
  wire [31:0] exp_418;
  wire [31:0] exp_417;
  wire [31:0] exp_416;
  wire [11:0] exp_415;
  wire [11:0] exp_414;
  wire [11:0] exp_413;
  wire [0:0] exp_367;
  wire [5:0] exp_366;
  wire [0:0] exp_412;
  wire [11:0] exp_408;
  wire [11:0] exp_411;
  wire [6:0] exp_409;
  wire [4:0] exp_410;
  wire [31:0] exp_197;
  wire [0:0] exp_200;
  wire [31:0] exp_199;
  wire [0:0] exp_205;
  wire [0:0] exp_184;
  wire [0:0] exp_179;
  wire [0:0] exp_176;
  wire [31:0] exp_175;
  wire [0:0] exp_178;
  wire [31:0] exp_177;
  wire [0:0] exp_183;
  wire [0:0] exp_155;
  wire [0:0] exp_150;
  wire [0:0] exp_147;
  wire [31:0] exp_146;
  wire [0:0] exp_149;
  wire [31:0] exp_148;
  wire [0:0] exp_154;
  wire [0:0] exp_26;
  wire [0:0] exp_21;
  wire [0:0] exp_18;
  wire [0:0] exp_17;
  wire [0:0] exp_20;
  wire [11:0] exp_19;
  wire [0:0] exp_25;
  wire [0:0] exp_4;
  wire [0:0] exp_13;
  wire [0:0] exp_138;
  wire [0:0] exp_15;
  wire [0:0] exp_6;
  wire [0:0] exp_217;
  wire [0:0] exp_502;
  wire [0:0] exp_501;
  wire [0:0] exp_137;
  wire [0:0] exp_132;
  wire [0:0] exp_136;
  wire [0:0] exp_134;
  wire [0:0] exp_14;
  wire [0:0] exp_22;
  wire [0:0] exp_133;
  wire [0:0] exp_135;
  wire [0:0] exp_131;
  wire [0:0] exp_117;
  wire [0:0] exp_142;
  wire [0:0] exp_167;
  wire [0:0] exp_171;
  wire [0:0] exp_186;
  wire [0:0] exp_193;
  wire [0:0] exp_209;
  wire [0:0] exp_563;
  wire [0:0] exp_226;
  wire [0:0] exp_269;
  wire [31:0] exp_241;
  wire [0:0] exp_240;
  wire [1:0] exp_249;
  wire [4:0] exp_236;
  wire [0:0] exp_239;
  wire [0:0] exp_566;
  wire [0:0] exp_565;
  wire [4:0] exp_235;
  wire [31:0] exp_237;
  wire [31:0] exp_450;
  wire [0:0] exp_449;
  wire [31:0] exp_401;
  wire [2:0] exp_344;
  wire [2:0] exp_335;
  wire [0:0] exp_332;
  wire [0:0] exp_266;
  wire [6:0] exp_256;
  wire [6:0] exp_265;
  wire [0:0] exp_268;
  wire [6:0] exp_267;
  wire [0:0] exp_334;
  wire [2:0] exp_322;
  wire [0:0] exp_264;
  wire [4:0] exp_263;
  wire [0:0] exp_321;
  wire [2:0] exp_309;
  wire [0:0] exp_262;
  wire [5:0] exp_261;
  wire [0:0] exp_308;
  wire [2:0] exp_258;
  wire [0:0] exp_307;
  wire [0:0] exp_320;
  wire [0:0] exp_333;
  wire [0:0] exp_339;
  wire [0:0] exp_400;
  wire [31:0] exp_380;
  wire [0:0] exp_346;
  wire [0:0] exp_338;
  wire [0:0] exp_324;
  wire [0:0] exp_311;
  wire [0:0] exp_297;
  wire [0:0] exp_295;
  wire [0:0] exp_296;
  wire [0:0] exp_260;
  wire [4:0] exp_259;
  wire [0:0] exp_310;
  wire [0:0] exp_323;
  wire [0:0] exp_337;
  wire [0:0] exp_336;
  wire [0:0] exp_379;
  wire [31:0] exp_377;
  wire [31:0] exp_342;
  wire [31:0] exp_328;
  wire [0:0] exp_325;
  wire [0:0] exp_327;
  wire [31:0] exp_317;
  wire [0:0] exp_316;
  wire [31:0] exp_303;
  wire [0:0] exp_302;
  wire [31:0] exp_301;
  wire [31:0] exp_299;
  wire [19:0] exp_298;
  wire [3:0] exp_300;
  wire [31:0] exp_315;
  wire [31:0] exp_313;
  wire [19:0] exp_312;
  wire [3:0] exp_314;
  wire [31:0] exp_326;
  wire [31:0] exp_343;
  wire [31:0] exp_331;
  wire [0:0] exp_329;
  wire [0:0] exp_330;
  wire [31:0] exp_319;
  wire [0:0] exp_318;
  wire [31:0] exp_306;
  wire [0:0] exp_305;
  wire [31:0] exp_290;
  wire [0:0] exp_289;
  wire [31:0] exp_284;
  wire [0:0] exp_280;
  wire [4:0] exp_255;
  wire [0:0] exp_279;
  wire [0:0] exp_283;
  wire [31:0] exp_272;
  wire [0:0] exp_252;
  wire [0:0] exp_576;
  wire [0:0] exp_575;
  wire [0:0] exp_574;
  wire [0:0] exp_573;
  wire [4:0] exp_234;
  wire [0:0] exp_271;
  wire [31:0] exp_248;
  wire [0:0] exp_247;
  wire [1:0] exp_250;
  wire [4:0] exp_243;
  wire [0:0] exp_246;
  wire [0:0] exp_568;
  wire [0:0] exp_567;
  wire [4:0] exp_242;
  wire [31:0] exp_244;
  wire [31:0] exp_253;
  wire [31:0] exp_282;
  wire [0:0] exp_281;
  wire [31:0] exp_288;
  wire [31:0] exp_285;
  wire [31:0] exp_287;
  wire [11:0] exp_286;
  wire [31:0] exp_304;
  wire [31:0] exp_232;
  wire [0:0] exp_231;
  wire [31:0] exp_378;
  wire [31:0] exp_382;
  wire [31:0] exp_381;
  wire [5:0] exp_376;
  wire [5:0] exp_375;
  wire [5:0] exp_374;
  wire [4:0] exp_345;
  wire [4:0] exp_294;
  wire [0:0] exp_293;
  wire [4:0] exp_292;
  wire [4:0] exp_257;
  wire [31:0] exp_398;
  wire [1:0] exp_384;
  wire [0:0] exp_383;
  wire [31:0] exp_399;
  wire [1:0] exp_390;
  wire [0:0] exp_389;
  wire [31:0] exp_386;
  wire [31:0] exp_385;
  wire [31:0] exp_388;
  wire [31:0] exp_387;
  wire [31:0] exp_391;
  wire [31:0] exp_395;
  wire [32:0] exp_394;
  wire [32:0] exp_392;
  wire [0:0] exp_373;
  wire [0:0] exp_347;
  wire [0:0] exp_291;
  wire [0:0] exp_372;
  wire [0:0] exp_371;
  wire [0:0] exp_370;
  wire [32:0] exp_393;
  wire [31:0] exp_396;
  wire [31:0] exp_397;
  wire [31:0] exp_448;
  wire [0:0] exp_447;
  wire [31:0] exp_438;
  wire [7:0] exp_437;
  wire [7:0] exp_436;
  wire [7:0] exp_431;
  wire [1:0] exp_422;
  wire [1:0] exp_421;
  wire [1:0] exp_420;
  wire [0:0] exp_430;
  wire [7:0] exp_426;
  wire [31:0] exp_214;
  wire [31:0] exp_204;
  wire [0:0] exp_203;
  wire [31:0] exp_182;
  wire [0:0] exp_181;
  wire [31:0] exp_153;
  wire [0:0] exp_152;
  wire [31:0] exp_24;
  wire [0:0] exp_23;
  wire [31:0] exp_3;
  wire [31:0] exp_12;
  wire [31:0] exp_119;
  wire [31:0] exp_130;
  wire [23:0] exp_129;
  wire [15:0] exp_128;
  wire [7:0] exp_54;
  wire [0:0] exp_53;
  wire [0:0] exp_121;
  wire [9:0] exp_49;
  wire [29:0] exp_120;
  wire [31:0] exp_10;
  wire [0:0] exp_52;
  wire [0:0] exp_116;
  wire [0:0] exp_114;
  wire [0:0] exp_115;
  wire [3:0] exp_16;
  wire [3:0] exp_7;
  wire [3:0] exp_218;
  wire [3:0] exp_499;
  wire [0:0] exp_498;
  wire [3:0] exp_486;
  wire [3:0] exp_482;
  wire [1:0] exp_485;
  wire [1:0] exp_484;
  wire [1:0] exp_483;
  wire [3:0] exp_491;
  wire [3:0] exp_487;
  wire [0:0] exp_490;
  wire [0:0] exp_489;
  wire [0:0] exp_488;
  wire [3:0] exp_492;
  wire [3:0] exp_493;
  wire [3:0] exp_494;
  wire [3:0] exp_495;
  wire [3:0] exp_496;
  wire [3:0] exp_497;
  wire [9:0] exp_48;
  wire [29:0] exp_112;
  wire [7:0] exp_50;
  wire [7:0] exp_113;
  wire [31:0] exp_11;
  wire [31:0] exp_2;
  wire [31:0] exp_213;
  wire [31:0] exp_481;
  wire [0:0] exp_480;
  wire [31:0] exp_468;
  wire [0:0] exp_467;
  wire [31:0] exp_454;
  wire [7:0] exp_453;
  wire [7:0] exp_452;
  wire [7:0] exp_451;
  wire [31:0] exp_341;
  wire [31:0] exp_462;
  wire [3:0] exp_461;
  wire [31:0] exp_464;
  wire [4:0] exp_463;
  wire [31:0] exp_466;
  wire [4:0] exp_465;
  wire [31:0] exp_472;
  wire [0:0] exp_425;
  wire [0:0] exp_424;
  wire [0:0] exp_423;
  wire [0:0] exp_471;
  wire [31:0] exp_458;
  wire [15:0] exp_457;
  wire [15:0] exp_456;
  wire [15:0] exp_455;
  wire [31:0] exp_470;
  wire [4:0] exp_469;
  wire [31:0] exp_474;
  wire [31:0] exp_473;
  wire [31:0] exp_460;
  wire [31:0] exp_459;
  wire [31:0] exp_475;
  wire [31:0] exp_476;
  wire [31:0] exp_477;
  wire [31:0] exp_478;
  wire [31:0] exp_479;
  wire [7:0] exp_47;
  wire [7:0] exp_75;
  wire [0:0] exp_74;
  wire [0:0] exp_88;
  wire [9:0] exp_70;
  wire [29:0] exp_87;
  wire [0:0] exp_73;
  wire [0:0] exp_84;
  wire [9:0] exp_69;
  wire [31:0] exp_83;
  wire [7:0] exp_71;
  wire [0:0] exp_46;
  wire [0:0] exp_123;
  wire [9:0] exp_42;
  wire [29:0] exp_122;
  wire [0:0] exp_45;
  wire [0:0] exp_111;
  wire [0:0] exp_109;
  wire [0:0] exp_110;
  wire [9:0] exp_41;
  wire [29:0] exp_107;
  wire [7:0] exp_43;
  wire [7:0] exp_108;
  wire [7:0] exp_40;
  wire [7:0] exp_68;
  wire [0:0] exp_67;
  wire [0:0] exp_90;
  wire [9:0] exp_63;
  wire [29:0] exp_89;
  wire [0:0] exp_66;
  wire [9:0] exp_62;
  wire [7:0] exp_64;
  wire [0:0] exp_39;
  wire [0:0] exp_125;
  wire [9:0] exp_35;
  wire [29:0] exp_124;
  wire [0:0] exp_38;
  wire [0:0] exp_106;
  wire [0:0] exp_104;
  wire [0:0] exp_105;
  wire [9:0] exp_34;
  wire [29:0] exp_102;
  wire [7:0] exp_36;
  wire [7:0] exp_103;
  wire [7:0] exp_33;
  wire [7:0] exp_61;
  wire [0:0] exp_60;
  wire [0:0] exp_92;
  wire [9:0] exp_56;
  wire [29:0] exp_91;
  wire [0:0] exp_59;
  wire [9:0] exp_55;
  wire [7:0] exp_57;
  wire [0:0] exp_32;
  wire [0:0] exp_127;
  wire [9:0] exp_28;
  wire [29:0] exp_126;
  wire [0:0] exp_31;
  wire [0:0] exp_101;
  wire [0:0] exp_99;
  wire [0:0] exp_100;
  wire [9:0] exp_27;
  wire [29:0] exp_97;
  wire [7:0] exp_29;
  wire [7:0] exp_98;
  wire [0:0] exp_118;
  wire [31:0] exp_141;
  wire [31:0] exp_157;
  wire [31:0] exp_164;
  wire [0:0] exp_159;
  wire [31:0] exp_158;
  wire [0:0] exp_163;
  wire [31:0] exp_161;
  wire [0:0] exp_160;
  wire [0:0] exp_162;
  wire [0:0] exp_156;
  wire [31:0] exp_170;
  wire [31:0] exp_189;
  wire [31:0] exp_192;
  wire [31:0] exp_207;
  wire [7:0] exp_427;
  wire [7:0] exp_428;
  wire [7:0] exp_429;
  wire [31:0] exp_441;
  wire [15:0] exp_440;
  wire [15:0] exp_439;
  wire [15:0] exp_435;
  wire [0:0] exp_434;
  wire [15:0] exp_432;
  wire [15:0] exp_433;
  wire [31:0] exp_442;
  wire [31:0] exp_443;
  wire [31:0] exp_444;
  wire [31:0] exp_445;
  wire [31:0] exp_446;
  wire [31:0] exp_276;
  wire [0:0] exp_275;
  wire [0:0] exp_505;
  wire [0:0] exp_518;
  wire [0:0] exp_519;
  wire [0:0] exp_506;
  wire [0:0] exp_507;
  wire [0:0] exp_512;
  wire [31:0] exp_509;
  wire [31:0] exp_508;
  wire [31:0] exp_511;
  wire [31:0] exp_510;
  wire [0:0] exp_517;
  wire [31:0] exp_514;
  wire [31:0] exp_513;
  wire [31:0] exp_516;
  wire [31:0] exp_515;
  wire [0:0] exp_580;
  wire [31:0] exp_579;
  wire [2:0] exp_578;
  wire [32:0] exp_562;
  wire [0:0] exp_561;
  wire [31:0] exp_552;
  wire [31:0] exp_551;
  wire [0:0] exp_550;
  wire [31:0] exp_537;
  wire [12:0] exp_536;
  wire [12:0] exp_535;
  wire [12:0] exp_534;
  wire [11:0] exp_533;
  wire [7:0] exp_532;
  wire [1:0] exp_531;
  wire [0:0] exp_526;
  wire [0:0] exp_527;
  wire [5:0] exp_528;
  wire [3:0] exp_529;
  wire [0:0] exp_530;
  wire [31:0] exp_549;
  wire [20:0] exp_548;
  wire [20:0] exp_547;
  wire [20:0] exp_546;
  wire [19:0] exp_545;
  wire [9:0] exp_544;
  wire [8:0] exp_543;
  wire [0:0] exp_538;
  wire [7:0] exp_539;
  wire [0:0] exp_540;
  wire [9:0] exp_541;
  wire [0:0] exp_542;
  wire [31:0] exp_349;
  wire [32:0] exp_560;
  wire [32:0] exp_559;
  wire [31:0] exp_557;
  wire [31:0] exp_556;
  wire [11:0] exp_555;
  wire [11:0] exp_554;
  wire [11:0] exp_553;
  wire [32:0] exp_558;
  wire [0:0] exp_229;
  wire [0:0] exp_80;
  wire [9:0] exp_76;
  wire [7:0] exp_78;
  wire [0:0] exp_9;
  wire [1:0] exp_364;
  wire [0:0] exp_173;
  wire [31:0] exp_169;
  wire [0:0] exp_211;
  wire [0:0] exp_194;
  wire [0:0] exp_202;
  wire [0:0] exp_210;
  wire [0:0] exp_195;

  assign exp_188 = exp_172 & exp_173;
  assign exp_172 = exp_180;
  assign exp_180 = exp_5 & exp_179;
  assign exp_5 = exp_216;
  assign exp_216 = exp_500;
  assign exp_500 = exp_365 | exp_367;
  assign exp_365 = exp_350 == exp_364;
  assign exp_350 = exp_348[6:0];

      reg [31:0] exp_348_reg = 0;
      always@(posedge clk) begin
        if (exp_339) begin
          exp_348_reg <= exp_96;
        end
      end
      assign exp_348 = exp_348_reg;
    
      reg [31:0] exp_96_reg = 0;
      always@(posedge clk) begin
        if (exp_9) begin
          exp_96_reg <= exp_95;
        end
      end
      assign exp_96 = exp_96_reg;
      assign exp_95 = {exp_94, exp_61};  assign exp_94 = {exp_93, exp_68};  assign exp_93 = {exp_82, exp_75};  assign exp_81 = exp_86;
  assign exp_86 = 1;
  assign exp_77 = exp_85;
  assign exp_85 = exp_8[31:2];
  assign exp_8 = exp_230;

      reg [31:0] exp_230_reg = 0;
      always@(posedge clk) begin
        if (exp_229) begin
          exp_230_reg <= exp_581;
        end
      end
      assign exp_230 = exp_230_reg;
    
  reg [32:0] exp_581_reg;
  always@(*) begin
    case (exp_577)
      0:exp_581_reg <= exp_579;
      1:exp_581_reg <= exp_562;
      default:exp_581_reg <= exp_580;
    endcase
  end
  assign exp_581 = exp_581_reg;
  assign exp_577 = exp_525 & exp_228;
  assign exp_525 = exp_503 | exp_524;
  assign exp_503 = exp_361 | exp_363;
  assign exp_361 = exp_350 == exp_360;
  assign exp_360 = 111;
  assign exp_363 = exp_350 == exp_362;
  assign exp_362 = 103;

  reg [0:0] exp_524_reg;
  always@(*) begin
    case (exp_369)
      0:exp_524_reg <= exp_522;
      1:exp_524_reg <= exp_521;
      default:exp_524_reg <= exp_523;
    endcase
  end
  assign exp_524 = exp_524_reg;
  assign exp_369 = exp_350 == exp_368;
  assign exp_368 = 99;
  assign exp_523 = 0;
  assign exp_522 = 0;

  reg [0:0] exp_521_reg;
  always@(*) begin
    case (exp_351)
      0:exp_521_reg <= exp_504;
      1:exp_521_reg <= exp_505;
      2:exp_521_reg <= exp_518;
      3:exp_521_reg <= exp_519;
      4:exp_521_reg <= exp_506;
      5:exp_521_reg <= exp_507;
      6:exp_521_reg <= exp_512;
      7:exp_521_reg <= exp_517;
      default:exp_521_reg <= exp_520;
    endcase
  end
  assign exp_521 = exp_521_reg;
  assign exp_351 = exp_348[14:12];
  assign exp_520 = 0;
  assign exp_504 = exp_340 == exp_341;

      reg [31:0] exp_340_reg = 0;
      always@(posedge clk) begin
        if (exp_339) begin
          exp_340_reg <= exp_278;
        end
      end
      assign exp_340 = exp_340_reg;
    
  reg [31:0] exp_278_reg;
  always@(*) begin
    case (exp_274)
      0:exp_278_reg <= exp_270;
      1:exp_278_reg <= exp_276;
      default:exp_278_reg <= exp_277;
    endcase
  end
  assign exp_278 = exp_278_reg;
  assign exp_274 = exp_254 == exp_273;
  assign exp_254 = exp_96[19:15];
  assign exp_273 = 0;
  assign exp_277 = 0;

  reg [31:0] exp_270_reg;
  always@(*) begin
    case (exp_251)
      0:exp_270_reg <= exp_241;
      1:exp_270_reg <= exp_253;
      default:exp_270_reg <= exp_269;
    endcase
  end
  assign exp_270 = exp_270_reg;
  assign exp_251 = exp_572;
  assign exp_572 = exp_571 & exp_220;
  assign exp_571 = exp_570 & exp_228;
  assign exp_570 = exp_569 & exp_407;
  assign exp_569 = exp_233 == exp_564;
  assign exp_233 = exp_96[19:15];
  assign exp_564 = exp_348[11:7];
  assign exp_407 = exp_406 | exp_365;
  assign exp_406 = exp_405 | exp_359;
  assign exp_405 = exp_404 | exp_357;
  assign exp_404 = exp_403 | exp_363;
  assign exp_403 = exp_402 | exp_361;
  assign exp_402 = exp_353 | exp_355;
  assign exp_353 = exp_350 == exp_352;
  assign exp_352 = 19;
  assign exp_355 = exp_350 == exp_354;
  assign exp_354 = 51;
  assign exp_357 = exp_350 == exp_356;
  assign exp_356 = 55;
  assign exp_359 = exp_350 == exp_358;
  assign exp_358 = 23;

      reg [0:0] exp_228_reg = 0;
      always@(posedge clk) begin
        if (exp_220) begin
          exp_228_reg <= exp_227;
        end
      end
      assign exp_228 = exp_228_reg;
      assign exp_227 = exp_225 & exp_226;

      reg [0:0] exp_225_reg = 0;
      always@(posedge clk) begin
        if (exp_220) begin
          exp_225_reg <= exp_224;
        end
      end
      assign exp_225 = exp_225_reg;
      assign exp_224 = exp_222 & exp_223;
  assign exp_222 = 1;
  assign exp_223 = ~exp_221;
  assign exp_221 = exp_582;
  assign exp_582 = exp_228 & exp_525;
  assign exp_220 = ~exp_219;
  assign exp_219 = exp_586;
  assign exp_586 = exp_228 & exp_585;
  assign exp_585 = exp_584 | exp_563;
  assign exp_584 = exp_216 & exp_583;
  assign exp_583 = ~exp_215;
  assign exp_215 = exp_206;

  reg [0:0] exp_206_reg;
  always@(*) begin
    case (exp_201)
      0:exp_206_reg <= exp_184;
      1:exp_206_reg <= exp_193;
      default:exp_206_reg <= exp_205;
    endcase
  end
  assign exp_206 = exp_206_reg;
  assign exp_201 = exp_198 & exp_200;
  assign exp_198 = exp_1 >= exp_197;
  assign exp_1 = exp_212;
  assign exp_212 = exp_419;
  assign exp_419 = exp_418 + exp_417;
  assign exp_418 = 0;
  assign exp_417 = exp_340 + exp_416;
  assign exp_416 = $signed(exp_415);
  assign exp_415 = exp_414 + exp_413;
  assign exp_414 = 0;

  reg [11:0] exp_413_reg;
  always@(*) begin
    case (exp_367)
      0:exp_413_reg <= exp_408;
      1:exp_413_reg <= exp_411;
      default:exp_413_reg <= exp_412;
    endcase
  end
  assign exp_413 = exp_413_reg;
  assign exp_367 = exp_350 == exp_366;
  assign exp_366 = 35;
  assign exp_412 = 0;
  assign exp_408 = exp_348[31:20];
  assign exp_411 = {exp_409, exp_410};  assign exp_409 = exp_348[31:25];
  assign exp_410 = exp_348[11:7];
  assign exp_197 = 2147483660;
  assign exp_200 = exp_1 <= exp_199;
  assign exp_199 = 2147483660;
  assign exp_205 = 0;

  reg [0:0] exp_184_reg;
  always@(*) begin
    case (exp_179)
      0:exp_184_reg <= exp_155;
      1:exp_184_reg <= exp_171;
      default:exp_184_reg <= exp_183;
    endcase
  end
  assign exp_184 = exp_184_reg;
  assign exp_179 = exp_176 & exp_178;
  assign exp_176 = exp_1 >= exp_175;
  assign exp_175 = 2147483656;
  assign exp_178 = exp_1 <= exp_177;
  assign exp_177 = 2147483656;
  assign exp_183 = 0;

  reg [0:0] exp_155_reg;
  always@(*) begin
    case (exp_150)
      0:exp_155_reg <= exp_26;
      1:exp_155_reg <= exp_142;
      default:exp_155_reg <= exp_154;
    endcase
  end
  assign exp_155 = exp_155_reg;
  assign exp_150 = exp_147 & exp_149;
  assign exp_147 = exp_1 >= exp_146;
  assign exp_146 = 2147483648;
  assign exp_149 = exp_1 <= exp_148;
  assign exp_148 = 2147483648;
  assign exp_154 = 0;

  reg [0:0] exp_26_reg;
  always@(*) begin
    case (exp_21)
      0:exp_26_reg <= exp_4;
      1:exp_26_reg <= exp_13;
      default:exp_26_reg <= exp_25;
    endcase
  end
  assign exp_26 = exp_26_reg;
  assign exp_21 = exp_18 & exp_20;
  assign exp_18 = exp_1 >= exp_17;
  assign exp_17 = 0;
  assign exp_20 = exp_1 <= exp_19;
  assign exp_19 = 4092;
  assign exp_25 = 0;
  assign exp_4 = 0;
  assign exp_13 = exp_138;

  reg [0:0] exp_138_reg;
  always@(*) begin
    case (exp_15)
      0:exp_138_reg <= exp_132;
      1:exp_138_reg <= exp_117;
      default:exp_138_reg <= exp_137;
    endcase
  end
  assign exp_138 = exp_138_reg;
  assign exp_15 = exp_6;
  assign exp_6 = exp_217;
  assign exp_217 = exp_502;
  assign exp_502 = exp_501 + exp_367;
  assign exp_501 = 0;
  assign exp_137 = 0;

      reg [0:0] exp_132_reg = 0;
      always@(posedge clk) begin
        if (exp_131) begin
          exp_132_reg <= exp_136;
        end
      end
      assign exp_132 = exp_132_reg;
      assign exp_136 = exp_134 & exp_135;
  assign exp_134 = exp_14 & exp_133;
  assign exp_14 = exp_22;
  assign exp_22 = exp_5 & exp_21;
  assign exp_133 = ~exp_15;
  assign exp_135 = ~exp_132;
  assign exp_131 = 1;
  assign exp_117 = 1;
  assign exp_142 = exp_167;
  assign exp_167 = 1;
  assign exp_171 = exp_186;
  assign exp_186 = stdout_ready_in;
  assign exp_193 = exp_209;
  assign exp_209 = stdin_valid_in;
  assign exp_563 = 0;
  assign exp_226 = ~exp_221;
  assign exp_269 = 0;

  //Create RAM
  reg [31:0] exp_241_ram [31:0];

  //Implement RAM port (Asynchronous)
  always@(posedge clk) begin
    if (exp_239) begin
      exp_241_ram[exp_235] <= exp_237;
    end
  end
  assign exp_241 = exp_241_ram[exp_236];
  assign exp_240 = exp_249;
  assign exp_249 = 1;
  assign exp_236 = exp_233;
  assign exp_239 = exp_566;
  assign exp_566 = exp_565 & exp_220;
  assign exp_565 = exp_407 & exp_228;
  assign exp_235 = exp_564;
  assign exp_237 = exp_450;

  reg [31:0] exp_450_reg;
  always@(*) begin
    case (exp_365)
      0:exp_450_reg <= exp_401;
      1:exp_450_reg <= exp_448;
      default:exp_450_reg <= exp_449;
    endcase
  end
  assign exp_450 = exp_450_reg;
  assign exp_449 = 0;

  reg [31:0] exp_401_reg;
  always@(*) begin
    case (exp_344)
      0:exp_401_reg <= exp_380;
      1:exp_401_reg <= exp_382;
      2:exp_401_reg <= exp_398;
      3:exp_401_reg <= exp_399;
      4:exp_401_reg <= exp_391;
      5:exp_401_reg <= exp_395;
      6:exp_401_reg <= exp_396;
      7:exp_401_reg <= exp_397;
      default:exp_401_reg <= exp_400;
    endcase
  end
  assign exp_401 = exp_401_reg;

      reg [2:0] exp_344_reg = 0;
      always@(posedge clk) begin
        if (exp_339) begin
          exp_344_reg <= exp_335;
        end
      end
      assign exp_344 = exp_344_reg;
    
  reg [2:0] exp_335_reg;
  always@(*) begin
    case (exp_332)
      0:exp_335_reg <= exp_322;
      1:exp_335_reg <= exp_333;
      default:exp_335_reg <= exp_334;
    endcase
  end
  assign exp_335 = exp_335_reg;
  assign exp_332 = exp_266 | exp_268;
  assign exp_266 = exp_256 == exp_265;
  assign exp_256 = exp_96[6:0];
  assign exp_265 = 111;
  assign exp_268 = exp_256 == exp_267;
  assign exp_267 = 103;
  assign exp_334 = 0;

  reg [2:0] exp_322_reg;
  always@(*) begin
    case (exp_264)
      0:exp_322_reg <= exp_309;
      1:exp_322_reg <= exp_320;
      default:exp_322_reg <= exp_321;
    endcase
  end
  assign exp_322 = exp_322_reg;
  assign exp_264 = exp_256 == exp_263;
  assign exp_263 = 23;
  assign exp_321 = 0;

  reg [2:0] exp_309_reg;
  always@(*) begin
    case (exp_262)
      0:exp_309_reg <= exp_258;
      1:exp_309_reg <= exp_307;
      default:exp_309_reg <= exp_308;
    endcase
  end
  assign exp_309 = exp_309_reg;
  assign exp_262 = exp_256 == exp_261;
  assign exp_261 = 55;
  assign exp_308 = 0;
  assign exp_258 = exp_96[14:12];
  assign exp_307 = 0;
  assign exp_320 = 0;
  assign exp_333 = 0;
  assign exp_339 = exp_220 & exp_225;
  assign exp_400 = 0;

  reg [31:0] exp_380_reg;
  always@(*) begin
    case (exp_346)
      0:exp_380_reg <= exp_377;
      1:exp_380_reg <= exp_378;
      default:exp_380_reg <= exp_379;
    endcase
  end
  assign exp_380 = exp_380_reg;

      reg [0:0] exp_346_reg = 0;
      always@(posedge clk) begin
        if (exp_339) begin
          exp_346_reg <= exp_338;
        end
      end
      assign exp_346 = exp_346_reg;
      assign exp_338 = exp_324 & exp_337;
  assign exp_324 = exp_311 & exp_323;
  assign exp_311 = exp_297 & exp_310;
  assign exp_297 = exp_295 & exp_296;
  assign exp_295 = exp_96[30:30];
  assign exp_296 = ~exp_260;
  assign exp_260 = exp_256 == exp_259;
  assign exp_259 = 19;
  assign exp_310 = ~exp_262;
  assign exp_323 = ~exp_264;
  assign exp_337 = ~exp_336;
  assign exp_336 = exp_266 | exp_268;
  assign exp_379 = 0;
  assign exp_377 = exp_342 + exp_343;

      reg [31:0] exp_342_reg = 0;
      always@(posedge clk) begin
        if (exp_339) begin
          exp_342_reg <= exp_328;
        end
      end
      assign exp_342 = exp_342_reg;
    
  reg [31:0] exp_328_reg;
  always@(*) begin
    case (exp_325)
      0:exp_328_reg <= exp_317;
      1:exp_328_reg <= exp_326;
      default:exp_328_reg <= exp_327;
    endcase
  end
  assign exp_328 = exp_328_reg;
  assign exp_325 = exp_266 | exp_268;
  assign exp_327 = 0;

  reg [31:0] exp_317_reg;
  always@(*) begin
    case (exp_264)
      0:exp_317_reg <= exp_303;
      1:exp_317_reg <= exp_315;
      default:exp_317_reg <= exp_316;
    endcase
  end
  assign exp_317 = exp_317_reg;
  assign exp_316 = 0;

  reg [31:0] exp_303_reg;
  always@(*) begin
    case (exp_262)
      0:exp_303_reg <= exp_278;
      1:exp_303_reg <= exp_301;
      default:exp_303_reg <= exp_302;
    endcase
  end
  assign exp_303 = exp_303_reg;
  assign exp_302 = 0;
  assign exp_301 = exp_299 << exp_300;
  assign exp_299 = exp_298;
  assign exp_298 = exp_96[31:12];
  assign exp_300 = 12;
  assign exp_315 = exp_313 << exp_314;
  assign exp_313 = exp_312;
  assign exp_312 = exp_96[31:12];
  assign exp_314 = 12;
  assign exp_326 = 4;

      reg [31:0] exp_343_reg = 0;
      always@(posedge clk) begin
        if (exp_339) begin
          exp_343_reg <= exp_331;
        end
      end
      assign exp_343 = exp_343_reg;
    
  reg [31:0] exp_331_reg;
  always@(*) begin
    case (exp_329)
      0:exp_331_reg <= exp_319;
      1:exp_331_reg <= exp_232;
      default:exp_331_reg <= exp_330;
    endcase
  end
  assign exp_331 = exp_331_reg;
  assign exp_329 = exp_266 | exp_268;
  assign exp_330 = 0;

  reg [31:0] exp_319_reg;
  always@(*) begin
    case (exp_264)
      0:exp_319_reg <= exp_306;
      1:exp_319_reg <= exp_232;
      default:exp_319_reg <= exp_318;
    endcase
  end
  assign exp_319 = exp_319_reg;
  assign exp_318 = 0;

  reg [31:0] exp_306_reg;
  always@(*) begin
    case (exp_262)
      0:exp_306_reg <= exp_290;
      1:exp_306_reg <= exp_304;
      default:exp_306_reg <= exp_305;
    endcase
  end
  assign exp_306 = exp_306_reg;
  assign exp_305 = 0;

  reg [31:0] exp_290_reg;
  always@(*) begin
    case (exp_260)
      0:exp_290_reg <= exp_284;
      1:exp_290_reg <= exp_288;
      default:exp_290_reg <= exp_289;
    endcase
  end
  assign exp_290 = exp_290_reg;
  assign exp_289 = 0;

  reg [31:0] exp_284_reg;
  always@(*) begin
    case (exp_280)
      0:exp_284_reg <= exp_272;
      1:exp_284_reg <= exp_282;
      default:exp_284_reg <= exp_283;
    endcase
  end
  assign exp_284 = exp_284_reg;
  assign exp_280 = exp_255 == exp_279;
  assign exp_255 = exp_96[24:20];
  assign exp_279 = 0;
  assign exp_283 = 0;

  reg [31:0] exp_272_reg;
  always@(*) begin
    case (exp_252)
      0:exp_272_reg <= exp_248;
      1:exp_272_reg <= exp_253;
      default:exp_272_reg <= exp_271;
    endcase
  end
  assign exp_272 = exp_272_reg;
  assign exp_252 = exp_576;
  assign exp_576 = exp_575 & exp_220;
  assign exp_575 = exp_574 & exp_228;
  assign exp_574 = exp_573 & exp_407;
  assign exp_573 = exp_234 == exp_564;
  assign exp_234 = exp_96[24:20];
  assign exp_271 = 0;

  //Create RAM
  reg [31:0] exp_248_ram [31:0];

  //Implement RAM port (Asynchronous)
  always@(posedge clk) begin
    if (exp_246) begin
      exp_248_ram[exp_242] <= exp_244;
    end
  end
  assign exp_248 = exp_248_ram[exp_243];
  assign exp_247 = exp_250;
  assign exp_250 = 1;
  assign exp_243 = exp_234;
  assign exp_246 = exp_568;
  assign exp_568 = exp_567 & exp_220;
  assign exp_567 = exp_407 & exp_228;
  assign exp_242 = exp_564;
  assign exp_244 = exp_450;
  assign exp_253 = exp_450;
  assign exp_282 = $signed(exp_281);
  assign exp_281 = 0;
  assign exp_288 = exp_285 + exp_287;
  assign exp_285 = 0;
  assign exp_287 = $signed(exp_286);
  assign exp_286 = exp_96[31:20];
  assign exp_304 = 0;

      reg [31:0] exp_232_reg = 0;
      always@(posedge clk) begin
        if (exp_231) begin
          exp_232_reg <= exp_230;
        end
      end
      assign exp_232 = exp_232_reg;
      assign exp_231 = exp_222 & exp_220;
  assign exp_378 = exp_342 - exp_343;
  assign exp_382 = exp_342 << exp_381;
  assign exp_381 = $signed(exp_376);
  assign exp_376 = exp_375 + exp_374;
  assign exp_375 = 0;
  assign exp_374 = exp_345;

      reg [4:0] exp_345_reg = 0;
      always@(posedge clk) begin
        if (exp_339) begin
          exp_345_reg <= exp_294;
        end
      end
      assign exp_345 = exp_345_reg;
    
  reg [4:0] exp_294_reg;
  always@(*) begin
    case (exp_260)
      0:exp_294_reg <= exp_292;
      1:exp_294_reg <= exp_257;
      default:exp_294_reg <= exp_293;
    endcase
  end
  assign exp_294 = exp_294_reg;
  assign exp_293 = 0;
  assign exp_292 = exp_290[4:0];
  assign exp_257 = exp_96[24:20];
  assign exp_398 = $signed(exp_384);
  assign exp_384 = exp_383;
  assign exp_383 = $signed(exp_342) < $signed(exp_343);
  assign exp_399 = $signed(exp_390);
  assign exp_390 = exp_389;
  assign exp_389 = exp_386 < exp_388;
  assign exp_386 = exp_385 + exp_342;
  assign exp_385 = 0;
  assign exp_388 = exp_387 + exp_343;
  assign exp_387 = 0;
  assign exp_391 = exp_342 ^ exp_343;
  assign exp_395 = exp_394[31:0];
  assign exp_394 = $signed(exp_392) >>> $signed(exp_393);
  assign exp_392 = {exp_373, exp_342};
  reg [0:0] exp_373_reg;
  always@(*) begin
    case (exp_347)
      0:exp_373_reg <= exp_371;
      1:exp_373_reg <= exp_370;
      default:exp_373_reg <= exp_372;
    endcase
  end
  assign exp_373 = exp_373_reg;

      reg [0:0] exp_347_reg = 0;
      always@(posedge clk) begin
        if (exp_339) begin
          exp_347_reg <= exp_291;
        end
      end
      assign exp_347 = exp_347_reg;
      assign exp_291 = exp_96[30:30];
  assign exp_372 = 0;
  assign exp_371 = 0;
  assign exp_370 = exp_342[31:31];
  assign exp_393 = $signed(exp_376);
  assign exp_396 = exp_342 | exp_343;
  assign exp_397 = exp_342 & exp_343;

  reg [31:0] exp_448_reg;
  always@(*) begin
    case (exp_351)
      0:exp_448_reg <= exp_438;
      1:exp_448_reg <= exp_441;
      2:exp_448_reg <= exp_214;
      3:exp_448_reg <= exp_442;
      4:exp_448_reg <= exp_443;
      5:exp_448_reg <= exp_444;
      6:exp_448_reg <= exp_445;
      7:exp_448_reg <= exp_446;
      default:exp_448_reg <= exp_447;
    endcase
  end
  assign exp_448 = exp_448_reg;
  assign exp_447 = 0;
  assign exp_438 = $signed(exp_437);
  assign exp_437 = exp_436 + exp_431;
  assign exp_436 = 0;

  reg [7:0] exp_431_reg;
  always@(*) begin
    case (exp_422)
      0:exp_431_reg <= exp_426;
      1:exp_431_reg <= exp_427;
      2:exp_431_reg <= exp_428;
      3:exp_431_reg <= exp_429;
      default:exp_431_reg <= exp_430;
    endcase
  end
  assign exp_431 = exp_431_reg;
  assign exp_422 = exp_421 + exp_420;
  assign exp_421 = 0;
  assign exp_420 = exp_419[1:0];
  assign exp_430 = 0;
  assign exp_426 = exp_214[7:0];
  assign exp_214 = exp_204;

  reg [31:0] exp_204_reg;
  always@(*) begin
    case (exp_201)
      0:exp_204_reg <= exp_182;
      1:exp_204_reg <= exp_192;
      default:exp_204_reg <= exp_203;
    endcase
  end
  assign exp_204 = exp_204_reg;
  assign exp_203 = 0;

  reg [31:0] exp_182_reg;
  always@(*) begin
    case (exp_179)
      0:exp_182_reg <= exp_153;
      1:exp_182_reg <= exp_170;
      default:exp_182_reg <= exp_181;
    endcase
  end
  assign exp_182 = exp_182_reg;
  assign exp_181 = 0;

  reg [31:0] exp_153_reg;
  always@(*) begin
    case (exp_150)
      0:exp_153_reg <= exp_24;
      1:exp_153_reg <= exp_141;
      default:exp_153_reg <= exp_152;
    endcase
  end
  assign exp_153 = exp_153_reg;
  assign exp_152 = 0;

  reg [31:0] exp_24_reg;
  always@(*) begin
    case (exp_21)
      0:exp_24_reg <= exp_3;
      1:exp_24_reg <= exp_12;
      default:exp_24_reg <= exp_23;
    endcase
  end
  assign exp_24 = exp_24_reg;
  assign exp_23 = 0;
  assign exp_3 = 0;
  assign exp_12 = exp_119;

      reg [31:0] exp_119_reg = 0;
      always@(posedge clk) begin
        if (exp_118) begin
          exp_119_reg <= exp_130;
        end
      end
      assign exp_119 = exp_119_reg;
      assign exp_130 = {exp_129, exp_33};  assign exp_129 = {exp_128, exp_40};  assign exp_128 = {exp_54, exp_47};
  //Create RAM
  reg [7:0] exp_54_ram [1023:0];


  //Initialise RAM contents
  initial
  begin
    exp_54_ram[0] = 0;
    exp_54_ram[1] = 0;
    exp_54_ram[2] = 0;
    exp_54_ram[3] = 0;
    exp_54_ram[4] = 0;
    exp_54_ram[5] = 0;
    exp_54_ram[6] = 0;
    exp_54_ram[7] = 0;
    exp_54_ram[8] = 0;
    exp_54_ram[9] = 0;
    exp_54_ram[10] = 0;
    exp_54_ram[11] = 0;
    exp_54_ram[12] = 0;
    exp_54_ram[13] = 0;
    exp_54_ram[14] = 0;
    exp_54_ram[15] = 0;
    exp_54_ram[16] = 0;
    exp_54_ram[17] = 0;
    exp_54_ram[18] = 0;
    exp_54_ram[19] = 0;
    exp_54_ram[20] = 0;
    exp_54_ram[21] = 0;
    exp_54_ram[22] = 0;
    exp_54_ram[23] = 0;
    exp_54_ram[24] = 0;
    exp_54_ram[25] = 0;
    exp_54_ram[26] = 0;
    exp_54_ram[27] = 0;
    exp_54_ram[28] = 0;
    exp_54_ram[29] = 0;
    exp_54_ram[30] = 0;
    exp_54_ram[31] = 0;
    exp_54_ram[32] = 63;
    exp_54_ram[33] = 7;
    exp_54_ram[34] = 0;
    exp_54_ram[35] = 108;
    exp_54_ram[36] = 111;
    exp_54_ram[37] = 33;
    exp_54_ram[38] = 0;
    exp_54_ram[39] = 0;
    exp_54_ram[40] = 0;
    exp_54_ram[41] = 0;
    exp_54_ram[42] = 0;
    exp_54_ram[43] = 0;
    exp_54_ram[44] = 0;
    exp_54_ram[45] = 0;
    exp_54_ram[46] = 0;
    exp_54_ram[47] = 254;
    exp_54_ram[48] = 255;
    exp_54_ram[49] = 0;
    exp_54_ram[50] = 18;
    exp_54_ram[51] = 0;
    exp_54_ram[52] = 0;
    exp_54_ram[53] = 252;
    exp_54_ram[54] = 0;
    exp_54_ram[55] = 0;
    exp_54_ram[56] = 0;
    exp_54_ram[57] = 0;
    exp_54_ram[58] = 0;
    exp_54_ram[59] = 1;
    exp_54_ram[60] = 0;
    exp_54_ram[61] = 255;
    exp_54_ram[62] = 0;
    exp_54_ram[63] = 0;
    exp_54_ram[64] = 1;
    exp_54_ram[65] = 8;
    exp_54_ram[66] = 251;
    exp_54_ram[67] = 0;
    exp_54_ram[68] = 0;
    exp_54_ram[69] = 0;
    exp_54_ram[70] = 1;
    exp_54_ram[71] = 0;
    exp_54_ram[72] = 128;
    exp_54_ram[73] = 0;
  end

  //Implement RAM port (Asynchronous)
  always@(posedge clk) begin
    if (exp_52) begin
      exp_54_ram[exp_48] <= exp_50;
    end
  end
  assign exp_54 = exp_54_ram[exp_49];


  //Additional RAM port (asynchronous)
  always@(posedge clk) begin
    if (exp_80) begin
        exp_54_ram[exp_76] <= exp_78;
    end
  end
  assign exp_82 = exp_54_ram[exp_77];
  assign exp_53 = exp_121;
  assign exp_121 = 1;
  assign exp_49 = exp_120;
  assign exp_120 = exp_10[31:2];
  assign exp_10 = exp_1;
  assign exp_52 = exp_116;
  assign exp_116 = exp_114 & exp_115;
  assign exp_114 = exp_14 & exp_15;
  assign exp_115 = exp_16[3:3];
  assign exp_16 = exp_7;
  assign exp_7 = exp_218;
  assign exp_218 = exp_499;

  reg [3:0] exp_499_reg;
  always@(*) begin
    case (exp_351)
      0:exp_499_reg <= exp_486;
      1:exp_499_reg <= exp_491;
      2:exp_499_reg <= exp_492;
      3:exp_499_reg <= exp_493;
      4:exp_499_reg <= exp_494;
      5:exp_499_reg <= exp_495;
      6:exp_499_reg <= exp_496;
      7:exp_499_reg <= exp_497;
      default:exp_499_reg <= exp_498;
    endcase
  end
  assign exp_499 = exp_499_reg;
  assign exp_498 = 0;
  assign exp_486 = exp_482 << exp_485;
  assign exp_482 = 1;
  assign exp_485 = exp_484 + exp_483;
  assign exp_484 = 0;
  assign exp_483 = exp_419[1:0];
  assign exp_491 = exp_487 << exp_490;
  assign exp_487 = 3;
  assign exp_490 = exp_489 + exp_488;
  assign exp_489 = 0;
  assign exp_488 = exp_419[1:1];
  assign exp_492 = 15;
  assign exp_493 = 0;
  assign exp_494 = 0;
  assign exp_495 = 0;
  assign exp_496 = 0;
  assign exp_497 = 0;
  assign exp_48 = exp_112;
  assign exp_112 = exp_10[31:2];
  assign exp_50 = exp_113;
  assign exp_113 = exp_11[31:24];
  assign exp_11 = exp_2;
  assign exp_2 = exp_213;
  assign exp_213 = exp_481;

  reg [31:0] exp_481_reg;
  always@(*) begin
    case (exp_351)
      0:exp_481_reg <= exp_468;
      1:exp_481_reg <= exp_472;
      2:exp_481_reg <= exp_474;
      3:exp_481_reg <= exp_475;
      4:exp_481_reg <= exp_476;
      5:exp_481_reg <= exp_477;
      6:exp_481_reg <= exp_478;
      7:exp_481_reg <= exp_479;
      default:exp_481_reg <= exp_480;
    endcase
  end
  assign exp_481 = exp_481_reg;
  assign exp_480 = 0;

  reg [31:0] exp_468_reg;
  always@(*) begin
    case (exp_422)
      0:exp_468_reg <= exp_454;
      1:exp_468_reg <= exp_462;
      2:exp_468_reg <= exp_464;
      3:exp_468_reg <= exp_466;
      default:exp_468_reg <= exp_467;
    endcase
  end
  assign exp_468 = exp_468_reg;
  assign exp_467 = 0;
  assign exp_454 = exp_453;
  assign exp_453 = exp_452 + exp_451;
  assign exp_452 = 0;
  assign exp_451 = exp_341[7:0];

      reg [31:0] exp_341_reg = 0;
      always@(posedge clk) begin
        if (exp_339) begin
          exp_341_reg <= exp_284;
        end
      end
      assign exp_341 = exp_341_reg;
      assign exp_462 = exp_454 << exp_461;
  assign exp_461 = 8;
  assign exp_464 = exp_454 << exp_463;
  assign exp_463 = 16;
  assign exp_466 = exp_454 << exp_465;
  assign exp_465 = 24;

  reg [31:0] exp_472_reg;
  always@(*) begin
    case (exp_425)
      0:exp_472_reg <= exp_458;
      1:exp_472_reg <= exp_470;
      default:exp_472_reg <= exp_471;
    endcase
  end
  assign exp_472 = exp_472_reg;
  assign exp_425 = exp_424 + exp_423;
  assign exp_424 = 0;
  assign exp_423 = exp_419[1:1];
  assign exp_471 = 0;
  assign exp_458 = exp_457;
  assign exp_457 = exp_456 + exp_455;
  assign exp_456 = 0;
  assign exp_455 = exp_341[15:0];
  assign exp_470 = exp_458 << exp_469;
  assign exp_469 = 16;
  assign exp_474 = exp_473 + exp_460;
  assign exp_473 = 0;
  assign exp_460 = exp_459 + exp_341;
  assign exp_459 = 0;
  assign exp_475 = 0;
  assign exp_476 = 0;
  assign exp_477 = 0;
  assign exp_478 = 0;
  assign exp_479 = 0;

  //Create RAM
  reg [7:0] exp_47_ram [1023:0];


  //Initialise RAM contents
  initial
  begin
    exp_47_ram[0] = 0;
    exp_47_ram[1] = 0;
    exp_47_ram[2] = 0;
    exp_47_ram[3] = 0;
    exp_47_ram[4] = 0;
    exp_47_ram[5] = 0;
    exp_47_ram[6] = 0;
    exp_47_ram[7] = 0;
    exp_47_ram[8] = 0;
    exp_47_ram[9] = 0;
    exp_47_ram[10] = 0;
    exp_47_ram[11] = 0;
    exp_47_ram[12] = 0;
    exp_47_ram[13] = 0;
    exp_47_ram[14] = 0;
    exp_47_ram[15] = 0;
    exp_47_ram[16] = 0;
    exp_47_ram[17] = 0;
    exp_47_ram[18] = 0;
    exp_47_ram[19] = 0;
    exp_47_ram[20] = 0;
    exp_47_ram[21] = 0;
    exp_47_ram[22] = 0;
    exp_47_ram[23] = 0;
    exp_47_ram[24] = 0;
    exp_47_ram[25] = 0;
    exp_47_ram[26] = 0;
    exp_47_ram[27] = 0;
    exp_47_ram[28] = 0;
    exp_47_ram[29] = 0;
    exp_47_ram[30] = 0;
    exp_47_ram[31] = 0;
    exp_47_ram[32] = 193;
    exp_47_ram[33] = 0;
    exp_47_ram[34] = 0;
    exp_47_ram[35] = 108;
    exp_47_ram[36] = 87;
    exp_47_ram[37] = 100;
    exp_47_ram[38] = 0;
    exp_47_ram[39] = 5;
    exp_47_ram[40] = 0;
    exp_47_ram[41] = 167;
    exp_47_ram[42] = 7;
    exp_47_ram[43] = 7;
    exp_47_ram[44] = 0;
    exp_47_ram[45] = 21;
    exp_47_ram[46] = 229;
    exp_47_ram[47] = 159;
    exp_47_ram[48] = 1;
    exp_47_ram[49] = 129;
    exp_47_ram[50] = 0;
    exp_47_ram[51] = 17;
    exp_47_ram[52] = 4;
    exp_47_ram[53] = 159;
    exp_47_ram[54] = 160;
    exp_47_ram[55] = 193;
    exp_47_ram[56] = 244;
    exp_47_ram[57] = 129;
    exp_47_ram[58] = 0;
    exp_47_ram[59] = 1;
    exp_47_ram[60] = 0;
    exp_47_ram[61] = 1;
    exp_47_ram[62] = 17;
    exp_47_ram[63] = 129;
    exp_47_ram[64] = 1;
    exp_47_ram[65] = 192;
    exp_47_ram[66] = 159;
    exp_47_ram[67] = 0;
    exp_47_ram[68] = 193;
    exp_47_ram[69] = 129;
    exp_47_ram[70] = 1;
    exp_47_ram[71] = 0;
    exp_47_ram[72] = 0;
    exp_47_ram[73] = 0;
  end

  //Implement RAM port (Asynchronous)
  always@(posedge clk) begin
    if (exp_45) begin
      exp_47_ram[exp_41] <= exp_43;
    end
  end
  assign exp_47 = exp_47_ram[exp_42];


  //Additional RAM port (asynchronous)
  always@(posedge clk) begin
    if (exp_73) begin
        exp_47_ram[exp_69] <= exp_71;
    end
  end
  assign exp_75 = exp_47_ram[exp_70];
  assign exp_74 = exp_88;
  assign exp_88 = 1;
  assign exp_70 = exp_87;
  assign exp_87 = exp_8[31:2];
  assign exp_73 = exp_84;
  assign exp_84 = 0;
  assign exp_69 = exp_83;
  assign exp_83 = 0;
  assign exp_71 = exp_83;
  assign exp_46 = exp_123;
  assign exp_123 = 1;
  assign exp_42 = exp_122;
  assign exp_122 = exp_10[31:2];
  assign exp_45 = exp_111;
  assign exp_111 = exp_109 & exp_110;
  assign exp_109 = exp_14 & exp_15;
  assign exp_110 = exp_16[2:2];
  assign exp_41 = exp_107;
  assign exp_107 = exp_10[31:2];
  assign exp_43 = exp_108;
  assign exp_108 = exp_11[23:16];

  //Create RAM
  reg [7:0] exp_40_ram [1023:0];


  //Initialise RAM contents
  initial
  begin
    exp_40_ram[0] = 0;
    exp_40_ram[1] = 1;
    exp_40_ram[2] = 1;
    exp_40_ram[3] = 2;
    exp_40_ram[4] = 2;
    exp_40_ram[5] = 3;
    exp_40_ram[6] = 3;
    exp_40_ram[7] = 4;
    exp_40_ram[8] = 4;
    exp_40_ram[9] = 5;
    exp_40_ram[10] = 5;
    exp_40_ram[11] = 6;
    exp_40_ram[12] = 6;
    exp_40_ram[13] = 7;
    exp_40_ram[14] = 7;
    exp_40_ram[15] = 8;
    exp_40_ram[16] = 8;
    exp_40_ram[17] = 9;
    exp_40_ram[18] = 9;
    exp_40_ram[19] = 10;
    exp_40_ram[20] = 10;
    exp_40_ram[21] = 11;
    exp_40_ram[22] = 11;
    exp_40_ram[23] = 12;
    exp_40_ram[24] = 12;
    exp_40_ram[25] = 13;
    exp_40_ram[26] = 13;
    exp_40_ram[27] = 14;
    exp_40_ram[28] = 14;
    exp_40_ram[29] = 15;
    exp_40_ram[30] = 15;
    exp_40_ram[31] = 1;
    exp_40_ram[32] = 1;
    exp_40_ram[33] = 0;
    exp_40_ram[34] = 0;
    exp_40_ram[35] = 101;
    exp_40_ram[36] = 32;
    exp_40_ram[37] = 108;
    exp_40_ram[38] = 0;
    exp_40_ram[39] = 7;
    exp_40_ram[40] = 5;
    exp_40_ram[41] = 135;
    exp_40_ram[42] = 71;
    exp_40_ram[43] = 20;
    exp_40_ram[44] = 128;
    exp_40_ram[45] = 5;
    exp_40_ram[46] = 160;
    exp_40_ram[47] = 240;
    exp_40_ram[48] = 1;
    exp_40_ram[49] = 36;
    exp_40_ram[50] = 36;
    exp_40_ram[51] = 38;
    exp_40_ram[52] = 5;
    exp_40_ram[53] = 240;
    exp_40_ram[54] = 7;
    exp_40_ram[55] = 32;
    exp_40_ram[56] = 32;
    exp_40_ram[57] = 36;
    exp_40_ram[58] = 5;
    exp_40_ram[59] = 1;
    exp_40_ram[60] = 128;
    exp_40_ram[61] = 1;
    exp_40_ram[62] = 38;
    exp_40_ram[63] = 36;
    exp_40_ram[64] = 4;
    exp_40_ram[65] = 5;
    exp_40_ram[66] = 240;
    exp_40_ram[67] = 0;
    exp_40_ram[68] = 32;
    exp_40_ram[69] = 36;
    exp_40_ram[70] = 1;
    exp_40_ram[71] = 128;
    exp_40_ram[72] = 0;
    exp_40_ram[73] = 0;
  end

  //Implement RAM port (Asynchronous)
  always@(posedge clk) begin
    if (exp_38) begin
      exp_40_ram[exp_34] <= exp_36;
    end
  end
  assign exp_40 = exp_40_ram[exp_35];


  //Additional RAM port (asynchronous)
  always@(posedge clk) begin
    if (exp_66) begin
        exp_40_ram[exp_62] <= exp_64;
    end
  end
  assign exp_68 = exp_40_ram[exp_63];
  assign exp_67 = exp_90;
  assign exp_90 = 1;
  assign exp_63 = exp_89;
  assign exp_89 = exp_8[31:2];
  assign exp_66 = exp_84;
  assign exp_62 = exp_83;
  assign exp_64 = exp_83;
  assign exp_39 = exp_125;
  assign exp_125 = 1;
  assign exp_35 = exp_124;
  assign exp_124 = exp_10[31:2];
  assign exp_38 = exp_106;
  assign exp_106 = exp_104 & exp_105;
  assign exp_104 = exp_14 & exp_15;
  assign exp_105 = exp_16[1:1];
  assign exp_34 = exp_102;
  assign exp_102 = exp_10[31:2];
  assign exp_36 = exp_103;
  assign exp_103 = exp_11[15:8];

  //Create RAM
  reg [7:0] exp_33_ram [1023:0];


  //Initialise RAM contents
  initial
  begin
    exp_33_ram[0] = 147;
    exp_33_ram[1] = 19;
    exp_33_ram[2] = 147;
    exp_33_ram[3] = 19;
    exp_33_ram[4] = 147;
    exp_33_ram[5] = 19;
    exp_33_ram[6] = 147;
    exp_33_ram[7] = 19;
    exp_33_ram[8] = 147;
    exp_33_ram[9] = 19;
    exp_33_ram[10] = 147;
    exp_33_ram[11] = 19;
    exp_33_ram[12] = 147;
    exp_33_ram[13] = 19;
    exp_33_ram[14] = 147;
    exp_33_ram[15] = 19;
    exp_33_ram[16] = 147;
    exp_33_ram[17] = 19;
    exp_33_ram[18] = 147;
    exp_33_ram[19] = 19;
    exp_33_ram[20] = 147;
    exp_33_ram[21] = 19;
    exp_33_ram[22] = 147;
    exp_33_ram[23] = 19;
    exp_33_ram[24] = 147;
    exp_33_ram[25] = 19;
    exp_33_ram[26] = 147;
    exp_33_ram[27] = 19;
    exp_33_ram[28] = 147;
    exp_33_ram[29] = 19;
    exp_33_ram[30] = 147;
    exp_33_ram[31] = 55;
    exp_33_ram[32] = 19;
    exp_33_ram[33] = 239;
    exp_33_ram[34] = 111;
    exp_33_ram[35] = 72;
    exp_33_ram[36] = 111;
    exp_33_ram[37] = 114;
    exp_33_ram[38] = 0;
    exp_33_ram[39] = 147;
    exp_33_ram[40] = 19;
    exp_33_ram[41] = 51;
    exp_33_ram[42] = 3;
    exp_33_ram[43] = 99;
    exp_33_ram[44] = 103;
    exp_33_ram[45] = 19;
    exp_33_ram[46] = 35;
    exp_33_ram[47] = 111;
    exp_33_ram[48] = 19;
    exp_33_ram[49] = 35;
    exp_33_ram[50] = 3;
    exp_33_ram[51] = 35;
    exp_33_ram[52] = 147;
    exp_33_ram[53] = 239;
    exp_33_ram[54] = 147;
    exp_33_ram[55] = 131;
    exp_33_ram[56] = 35;
    exp_33_ram[57] = 3;
    exp_33_ram[58] = 19;
    exp_33_ram[59] = 19;
    exp_33_ram[60] = 103;
    exp_33_ram[61] = 19;
    exp_33_ram[62] = 35;
    exp_33_ram[63] = 35;
    exp_33_ram[64] = 19;
    exp_33_ram[65] = 19;
    exp_33_ram[66] = 239;
    exp_33_ram[67] = 19;
    exp_33_ram[68] = 131;
    exp_33_ram[69] = 3;
    exp_33_ram[70] = 19;
    exp_33_ram[71] = 103;
    exp_33_ram[72] = 8;
    exp_33_ram[73] = 0;
  end

  //Implement RAM port (Asynchronous)
  always@(posedge clk) begin
    if (exp_31) begin
      exp_33_ram[exp_27] <= exp_29;
    end
  end
  assign exp_33 = exp_33_ram[exp_28];


  //Additional RAM port (asynchronous)
  always@(posedge clk) begin
    if (exp_59) begin
        exp_33_ram[exp_55] <= exp_57;
    end
  end
  assign exp_61 = exp_33_ram[exp_56];
  assign exp_60 = exp_92;
  assign exp_92 = 1;
  assign exp_56 = exp_91;
  assign exp_91 = exp_8[31:2];
  assign exp_59 = exp_84;
  assign exp_55 = exp_83;
  assign exp_57 = exp_83;
  assign exp_32 = exp_127;
  assign exp_127 = 1;
  assign exp_28 = exp_126;
  assign exp_126 = exp_10[31:2];
  assign exp_31 = exp_101;
  assign exp_101 = exp_99 & exp_100;
  assign exp_99 = exp_14 & exp_15;
  assign exp_100 = exp_16[0:0];
  assign exp_27 = exp_97;
  assign exp_97 = exp_10[31:2];
  assign exp_29 = exp_98;
  assign exp_98 = exp_11[7:0];
  assign exp_118 = 1;
  assign exp_141 = exp_157;

      reg [31:0] exp_157_reg = 0;
      always@(posedge clk) begin
        if (exp_156) begin
          exp_157_reg <= exp_164;
        end
      end
      assign exp_157 = exp_157_reg;
    
  reg [31:0] exp_164_reg;
  always@(*) begin
    case (exp_159)
      0:exp_164_reg <= exp_161;
      1:exp_164_reg <= exp_162;
      default:exp_164_reg <= exp_163;
    endcase
  end
  assign exp_164 = exp_164_reg;
  assign exp_159 = exp_157 == exp_158;
  assign exp_158 = 4294967295;
  assign exp_163 = 0;
  assign exp_161 = exp_157 + exp_160;
  assign exp_160 = 1;
  assign exp_162 = 0;
  assign exp_156 = 1;
  assign exp_170 = exp_189;
  assign exp_189 = 0;
  assign exp_192 = exp_207;
  assign exp_207 = stdin_data_in;
  assign exp_427 = exp_214[15:8];
  assign exp_428 = exp_214[23:16];
  assign exp_429 = exp_214[31:24];
  assign exp_441 = $signed(exp_440);
  assign exp_440 = exp_439 + exp_435;
  assign exp_439 = 0;

  reg [15:0] exp_435_reg;
  always@(*) begin
    case (exp_425)
      0:exp_435_reg <= exp_432;
      1:exp_435_reg <= exp_433;
      default:exp_435_reg <= exp_434;
    endcase
  end
  assign exp_435 = exp_435_reg;
  assign exp_434 = 0;
  assign exp_432 = exp_214[15:0];
  assign exp_433 = exp_214[31:16];
  assign exp_442 = 0;
  assign exp_443 = exp_431;
  assign exp_444 = exp_435;
  assign exp_445 = 0;
  assign exp_446 = 0;
  assign exp_276 = $signed(exp_275);
  assign exp_275 = 0;
  assign exp_505 = exp_340 != exp_341;
  assign exp_518 = 0;
  assign exp_519 = 0;
  assign exp_506 = $signed(exp_340) < $signed(exp_341);
  assign exp_507 = $signed(exp_340) >= $signed(exp_341);
  assign exp_512 = exp_509 < exp_511;
  assign exp_509 = exp_508 + exp_340;
  assign exp_508 = 0;
  assign exp_511 = exp_510 + exp_341;
  assign exp_510 = 0;
  assign exp_517 = exp_514 >= exp_516;
  assign exp_514 = exp_513 + exp_340;
  assign exp_513 = 0;
  assign exp_516 = exp_515 + exp_341;
  assign exp_515 = 0;
  assign exp_580 = 0;
  assign exp_579 = exp_230 + exp_578;
  assign exp_578 = 4;

  reg [32:0] exp_562_reg;
  always@(*) begin
    case (exp_363)
      0:exp_562_reg <= exp_552;
      1:exp_562_reg <= exp_560;
      default:exp_562_reg <= exp_561;
    endcase
  end
  assign exp_562 = exp_562_reg;
  assign exp_561 = 0;
  assign exp_552 = exp_551 + exp_349;

  reg [31:0] exp_551_reg;
  always@(*) begin
    case (exp_361)
      0:exp_551_reg <= exp_537;
      1:exp_551_reg <= exp_549;
      default:exp_551_reg <= exp_550;
    endcase
  end
  assign exp_551 = exp_551_reg;
  assign exp_550 = 0;
  assign exp_537 = $signed(exp_536);
  assign exp_536 = exp_535 + exp_534;
  assign exp_535 = 0;
  assign exp_534 = {exp_533, exp_530};  assign exp_533 = {exp_532, exp_529};  assign exp_532 = {exp_531, exp_528};  assign exp_531 = {exp_526, exp_527};  assign exp_526 = exp_348[31:31];
  assign exp_527 = exp_348[7:7];
  assign exp_528 = exp_348[30:25];
  assign exp_529 = exp_348[11:8];
  assign exp_530 = 0;
  assign exp_549 = $signed(exp_548);
  assign exp_548 = exp_547 + exp_546;
  assign exp_547 = 0;
  assign exp_546 = {exp_545, exp_542};  assign exp_545 = {exp_544, exp_541};  assign exp_544 = {exp_543, exp_540};  assign exp_543 = {exp_538, exp_539};  assign exp_538 = exp_348[31:31];
  assign exp_539 = exp_348[19:12];
  assign exp_540 = exp_348[20:20];
  assign exp_541 = exp_348[30:21];
  assign exp_542 = 0;

      reg [31:0] exp_349_reg = 0;
      always@(posedge clk) begin
        if (exp_339) begin
          exp_349_reg <= exp_232;
        end
      end
      assign exp_349 = exp_349_reg;
      assign exp_560 = exp_559 & exp_558;
  assign exp_559 = $signed(exp_557);
  assign exp_557 = exp_340 + exp_556;
  assign exp_556 = $signed(exp_555);
  assign exp_555 = exp_554 + exp_553;
  assign exp_554 = 0;
  assign exp_553 = exp_348[31:20];
  assign exp_558 = 4294967294;
  assign exp_229 = exp_222 & exp_220;
  assign exp_80 = exp_84;
  assign exp_76 = exp_83;
  assign exp_78 = exp_83;
  assign exp_9 = exp_231;
  assign exp_364 = 3;
  assign exp_173 = exp_6;
  assign exp_169 = exp_2;
  assign exp_211 = exp_194 & exp_210;
  assign exp_194 = exp_202;
  assign exp_202 = exp_5 & exp_201;
  assign exp_210 = ~exp_195;
  assign exp_195 = exp_6;
  assign stdout_valid_out = exp_188;
  assign stdout_out = exp_169;
  assign stdin_ready_out = exp_211;

endmodule